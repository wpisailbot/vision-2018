import cv2

cam = cv2.VideoCapture(0)

for x in dir(cv2.cv):
  if "CAP_PROP" in x:
    print(x+": "+str(cam.get(eval("cv2.cv."+x))))
