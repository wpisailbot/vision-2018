import cv2
import numpy as np
import hsv_consts
from hsv_detect import hsv_filt
import subprocess
import cam_params
import pdb


# Binary Image filtering
alpha = 0.75

def v4l2cmd(params):
  cmd_str = "v4l2-ctl -d /dev/video0"
  for param in params:
    cmd_str += " -c "+param+"="+str(params[param])
  print("Executing: "+cmd_str)
  out = subprocess.call(cmd_str, shell=True)
  print(out)

def main():
  cam = cv2.VideoCapture(0)
  fourcc = cv2.cv.CV_FOURCC('M','J','P','G')
  vidwriter = cv2.VideoWriter('out.mjpg', fourcc, 20, (640,480))
  v4l2cmd(cam_params.cam_params)

  accum = np.zeros((480,640),np.float32)

  while True:
    success, img = cam.read()
    if not success:
      print('Could not read camera')
      break
    print("writing image")
    vidwriter.write(img)

    cv2.imshow("Orig frame", img)

if __name__=='__main__':
  main()
