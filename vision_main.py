import cv2
import numpy as np
import hsv_consts
from hsv_detect import *
import subprocess
import cam_params
import pdb
import logging
from result_passer import ResultPasser
import threading
import signal
import time
import websocket
from boat_ws import *

# Binary Image filtering
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))

# Flag for stopping threads
should_run = True

# Flag for showing visualizations
visualize = False

# Threadsafe results passing
buoys_passer = ResultPasser()

logging.basicConfig(level=logging.DEBUG,
format='[%(levelname)s] (%(threadName)s) %(message)s')

def v4l2cmd(params):
  cmd_str = "v4l2-ctl -d /dev/video0"
  for param in params:
    cmd_str += " -c "+param+"="+str(params[param])
  print("Executing: "+cmd_str)
  out = subprocess.call(cmd_str, shell=True)
  print(out)

# Thread to send the current heading, and list of buoys
def ws_thread():
  last_timestamp = 0
  logging.debug("Starting")

  while(should_run):
    #try: 
      # Setup the websocket stuff
      ws = websocket.WebSocket()
      client = websocket.create_connection("ws://"+WS_SERVER+":"+WS_PORT)

      # Loop until signaled to exit
      while(should_run):
        # Get the list of buoys in the image
        value = buoys_passer.get()
        # Handle if data hasn't been set yet
        if value == None:
          continue
        # Split out the timestamp and data
        (new_conf, new_heading) = value
        client.send(JSONify(new_conf, new_heading))
        logging.debug(JSONify(new_conf, new_heading))
        time.sleep(0.1)

      client.close()
    #except:
    #  time.sleep(2)
    #  logging.debug("Connection died.  Restarting...")
  logging.debug("Done")
  return

def vision_thread():
  cam = cv2.VideoCapture(0)
  v4l2cmd(cam_params.cam_params)

  last_time = time.clock()
  logging.debug("Starting Image processing")
  count = 0
  
  while should_run:
    success, img = cam.read()
    if not success:
      logging.debug("Camera not connected")
      break

    binframe = hsv_filt(img, hsv_consts.lower_bounds,
                               hsv_consts.upper_bounds,
                               hsv_consts.wrap_bounds)
    denoiseframe = hsv_denoise(binframe, kernel, 2)
    boats = hsv_filt_buoy_contours(binframe, img, visualize)

    if visualize:
      cv2.imshow("Orig frame", img)
      cv2.imshow("Filt img", binframe)
      cv2.imshow("Denoise img", denoiseframe)
      cv2.waitKey(1)

    now_time = time.clock()
    if count%10 == 0:
      logging.debug("FPS: "+str(1/(now_time-last_time)))
    last_time = now_time
    count += 1

    if len(boats)!=0:
      # Assume the filter is good and only finds one boat
      # Also use the pixel location instead of an angle
      biggest = max(boats)
      bearing = (320-biggest[1])*.25*3.14159265/320
      conf = biggest[0]
      #logging.debug("Found buoy at "+str(bearing)+" conf: "+str(conf))
    else:
      bearing = 0
      conf = 0

    # Send the confidence as area, and bearing as right-hand rule in radians
    buoys_passer.set((conf, bearing))

# Threads and shutdown
threads = []
def kill_threads(signal, frame):
  logging.debug("Stopping threads")
  should_run = False
  for t in threads:
    t.join()
  logging.debug("Stopped all threads")

if __name__=='__main__':

  # Kickoff the websocket and vision threads
  t = threading.Thread(target=vision_thread, name="Img Proc")
  threads.append(t)
  t.start()
  t = threading.Thread(target=ws_thread, name="WS Sender")
  threads.append(t)
  t.start()

  # enable the handler for SIGINT
  signal.signal(signal.SIGINT, kill_threads)
  logging.debug("Registered SIGINT handler")
  # Allow the threads to run
  for t in threads:
    t.join() 
  logging.debug("Completed main")
