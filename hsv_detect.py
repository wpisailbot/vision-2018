import cv2
import numpy as np

def hsv_filt(frame, lower_bounds, upper_bounds, wrap_bounds):
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

  if wrap_bounds:
    # Wrap the bounds around the 180 HSV discontinuity
    lowside = cv2.inRange(hsv,
                    np.array([0,lower_bounds[1],lower_bounds[2]]),
                    np.array([lower_bounds[0],upper_bounds[1],upper_bounds[2]]))
    highside = cv2.inRange(hsv, 
                    np.array([upper_bounds[0],lower_bounds[1],lower_bounds[2]]),
                    np.array([180, upper_bounds[1], upper_bounds[2]]))
    binframe = cv2.bitwise_or(lowside, highside)
  else:
    binframe = cv2.inRange(hsv, lower_bounds, upper_bounds)
  return binframe

def hsv_denoise(binframe, kernel, iterations):
  temp = cv2.morphologyEx(binframe, cv2.MORPH_OPEN, kernel, iterations=iterations)
  return cv2.morphologyEx(temp, cv2.MORPH_CLOSE, kernel, iterations=iterations)

def hsv_filt_contours(binframe, imgframe, visualize):
  boats = []
  for cnt in cv2.findContours(binframe.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]:
    # Get the rotated rectangle surrounding the blob
    ((xcenter,ycenter), (width,height), ang) = cv2.minAreaRect(cnt)
    # Filter blobs by aspect ratio, area, and bottom 2/3 of image
    if max(width,height)>2*min(width,height) \
           and width*height > 4000 \
           and ycenter > 480*1/3:
      boats.append(((xcenter,ycenter),(width,height)))
      if visualize:
        box = cv2.cv.BoxPoints(((xcenter,ycenter),(width,height),ang))
        box = np.int0(box)
        cv2.drawContours(imgframe,[box],0,[0,0,255],2)
  return boats
