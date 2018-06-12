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
