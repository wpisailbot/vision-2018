import cv2
import numpy as np
import hsv_consts
from hsv_detect import *
import subprocess
import cam_params
import logging
import threading
import time

# Binary Image filtering
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))

logging.basicConfig(level=logging.DEBUG,
format='[%(levelname)s] (%(threadName)s) %(message)s')

def v4l2cmd(params):
  cmd_str = "v4l2-ctl -d /dev/video0"
  for param in params:
    cmd_str += " -c "+param+"="+str(params[param])
  print("Executing: "+cmd_str)
  out = subprocess.call(cmd_str, shell=True)
  print(out)

def vision_thread():
  cam = cv2.VideoCapture(0)
  v4l2cmd(cam_params.cam_params)

  last_time = time.clock()
  print("Starting Image processing")
  count = 0
  
  while True:
    success, img = cam.read()
    if not success:
      print("Camera not connected")
      break

    binframe = hsv_filt(img, hsv_consts.lower_bounds,
                               hsv_consts.upper_bounds,
                               hsv_consts.wrap_bounds)
    denoiseframe = hsv_denoise(binframe, kernel, 2)
    boats = hsv_filt_buoy_contours(binframe, img, True)


    cv2.imshow("Orig frame", img)
    cv2.imshow("Filt img", binframe)
    cv2.imshow("Denoise img", denoiseframe)
    cv2.waitKey(1)

    now_time = time.clock()
    if count%10 == 0:
      print("FPS: "+str(1/(now_time-last_time)))
    last_time = now_time
    count += 1
    time.sleep(1)

if __name__=='__main__':
  vision_thread()
