import base64
import cv2
import os
import numpy as np
from matplotlib import pyplot as plt

def cv2_to_base64(image):
    base64_str = cv2.imencode('.jpg', image)[1].tostring()
    base64_str = base64.b64encode(base64_str)
    return base64_str

def base64_to_cv2(base64_str):
    imgString = base64.b64decode(base64_str)
    nparr = np.frombuffer(imgString, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return image

if __name__ == '__main__':
  # cv2 转 base64
  image = cv2.imread("data/1.jpg")
  h, w, d = image.shape[:3]

  base64_str = cv2_to_base64(image)
  # print(base64_str)

  file_size = os.path.getsize("data/1.jpg")
  print("org file size: %d" % file_size)
  print("base64 string size: %d" % len(base64_str))
  print("image size: %d x %d - %d" % (w, h, d))
  print("image array size: %d" % (h*w*d))

  # base64 转 cv2
  with open("data/2.jpg", "rb") as f:
    base64_str = base64.b64encode(f.read())

  img = base64_to_cv2(base64_str)

  imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

  plt.imshow(imgrgb)
  plt.show()
