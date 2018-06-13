import cv2
import numpy as np
import hsv_consts
from hsv_detect import *
import subprocess
import cam_params
import pdb


# Binary Image filtering
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))

def main():
  water = cv2.imread('water.png')
  binwater = hsv_filt(water, hsv_consts.lower_bounds,
                             hsv_consts.upper_bounds,
                             hsv_consts.wrap_bounds)
  binwater = hsv_denoise(binwater, kernel, 2)
  boat = cv2.imread('boat.png')
  binboat = hsv_filt(boat, hsv_consts.lower_bounds,
                             hsv_consts.upper_bounds,
                             hsv_consts.wrap_bounds)
  binboat = hsv_denoise(binboat, kernel, 2)
  boat2 = cv2.imread('boat2.png')
  binboat2 = hsv_filt(boat2, hsv_consts.lower_bounds,
                             hsv_consts.upper_bounds,
                             hsv_consts.wrap_bounds)
  binboat2 = hsv_denoise(binboat2, kernel, 2)
  polar4 = cv2.imread('polar4.png')
  binpolar4 = hsv_filt(polar4, hsv_consts.lower_bounds,
                             hsv_consts.upper_bounds,
                             hsv_consts.wrap_bounds)
  binpolar4 = hsv_denoise(binpolar4, kernel, 2)
  polar5 = cv2.imread('polar5.png')
  binpolar5 = hsv_filt(polar5, hsv_consts.lower_bounds,
                             hsv_consts.upper_bounds,
                             hsv_consts.wrap_bounds)
  binpolar5 = hsv_denoise(binpolar5, kernel, 2)
  polar6 = cv2.imread('polar6.png')
  binpolar6 = hsv_filt(polar6, hsv_consts.lower_bounds,
                             hsv_consts.upper_bounds,
                             hsv_consts.wrap_bounds)
  binpolar6 = hsv_denoise(binpolar6, kernel, 2)


  # Attempt to process contours
  boats = []
  hsv_filt_contours(binpolar4, polar4, True)
  hsv_filt_contours(binpolar5, polar5, True)
  hsv_filt_contours(binpolar6, polar6, True)

  cv2.imshow("Original Water", water)
  cv2.imshow("Binary Water", binwater)
  cv2.imshow("Original Boat", boat)
  cv2.imshow("Binary Boat", binboat)
  cv2.imshow("Original Boat2", boat2)
  cv2.imshow("Binary Boat2", binboat2)
  cv2.imshow("Original Polar4", polar4)
  cv2.imshow("Binary Polar4", binpolar4)
  cv2.imshow("Original Polar5", polar5)
  cv2.imshow("Binary Polar5", binpolar5)
  cv2.imshow("Original Polar6", polar6)
  cv2.imshow("Binary Polar6", binpolar6)
  # Quit if the escape key is pressed
  while cv2.waitKey(1) != 27:
    pass

if __name__=='__main__':
  main()

