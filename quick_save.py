
import cv2
import numpy as np
import hsv_consts
from hsv_detect import hsv_filt
import subprocess
import pdb
import cam_params

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
  v4l2cmd(cam_params.cam_params)

  accum = np.zeros((480,640),np.float32)

  success, img = cam.read()
  success, img = cam.read()
  success, img = cam.read()
  success, img = cam.read()
  success, img = cam.read()
  success, img = cam.read()
  if not success:
    return

  cv2.imshow("Orig frame", img)
  cv2.imwrite("./out.png", img)

  while cv2.waitKey(1) != 27:
    pass

if __name__=='__main__':
  main()
