import cv2
import subprocess

def v4l2cmd(params):
  cmd_str = "v4l2-ctl -d /dev/video0"
  for param in params:
    cmd_str += " -c "+param+"="+str(params[param])
  print("Executing: "+cmd_str)
  out = subprocess.call(cmd_str, shell=True)
  print(out)

def main():
  cam = cv2.VideoCapture(0)

  v4l2cmd({'exposure_auto':1, 'exposure_absolute':157})
  success, img = cam.read()
  if not success:
    print('could not read frame')
    return
  print('showing image 1: ')
  cv2.imshow('webcam',img)
  v4l2cmd({'exposure_auto':1, 'exposure_absolute':400})
  success, img2 = cam.read()
  if not success:
    print('could not read frame')
    return
  print('showing image 2: ')
  cv2.imshow('webcam2',img2)
  while cv2.waitKey(0)!=27:
    pass
  print('done')
  cv2.destroyAllWindows()

if __name__=="__main__":
  main()
