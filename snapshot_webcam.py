import cv2

def show_webcam(mirror=False):
  cam = cv2.VideoCapture(0)
  ret_val, img = cam.read()
  if mirror:
    img = cv2.flip(img, 1)
  cv2.imshow('webcam', img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

def main():
  show_webcam(mirror=True)

if __name__ == "__main__":
  main()
