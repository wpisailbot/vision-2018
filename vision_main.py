import cv2
import hsv_consts
from hsv_detect import hsv_filt
import subprocess

# Image sensor exposure time 1-5000
exposure_time = 40
# Contrast
contrast = 55
# Brightness -64-64
brightness = 64
# Saturation 0-128
saturation = 110
# gain 0-100
gain = 0


def v4l2cmd(params):
  cmd_str = "v4l2-ctl -d /dev/video0"
  for param in params:
    cmd_str += " -c "+param+"="+str(params[param])
  print("Executing: "+cmd_str)
  out = subprocess.call(cmd_str, shell=True)
  print(out)

def main():
  cam = cv2.VideoCapture(0)
  v4l2cmd({'exposure_auto':1, 'exposure_absolute':exposure_time,
           'gain':gain,'saturation':saturation,
           'brightness':brightness,'contrast':contrast})

  while True:
    success, img = cam.read()
    if not success:
      break

    binframe = hsv_filt(img, hsv_consts.lower_bounds,
                               hsv_consts.upper_bounds,
                               hsv_consts.wrap_bounds)
    cv2.imshow("Orig frame", img)
    cv2.imshow("Filt img", binframe)
    # Quit if the escape key is pressed
    if cv2.waitKey(1) == 27:
      break

  # Do any final cleanup

if __name__=='__main__':
  main()
