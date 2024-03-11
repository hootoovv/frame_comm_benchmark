import requests
import requests_unixsocket

# import base64
import pybase64 as base64
import cv2
import numpy as np
import time
import platform

sys = platform.system()
if sys == "Linux":
  url = 'http+unix://%2Ftmp%2Ffastapi.sock'
else:
  url = "http://127.0.0.1:8000"

requests_unixsocket.monkeypatch()

# 读取视频
cap = cv2.VideoCapture('data/person.mp4')

# 调整显示视频窗口
cv2.namedWindow("video - press q to quit",0)
cv2.resizeWindow("video - press q to quit", 1280, 640)

# used to record the time when we processed last frame 
prev_frame_time = 0  
# used to record the time at which we processed current frame 
new_frame_time = 0
# font which we will be using to display FPS 
font = cv2.FONT_HERSHEY_SIMPLEX 

frame_drop_num=3
frame_drop_counter =0
frame_drop_time=[0,0,0]

while True:
  # time when we finish processing for this frame 
  new_frame_time = time.time()
  # Calculating the fps
  # fps will be number of frame processed in given time frame 
  # since their will be most of time error of 0.001 second 
  # we will be subtracting it to get more accurate result 
  fps = 1/(new_frame_time-prev_frame_time)
  
  frame_drop_time.append(fps)
  frame_drop_time.pop(0)      
  prev_frame_time = new_frame_time
    
  # 读取一帧视频
  ret, frame = cap.read()
  if frame is None:
      break
  
  id = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
  h, w, d = frame.shape[:3]
  
  # frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
  upload = False # test file upload and download
  if upload:
    params  = {"id": id, "w": w, "h": h, "d": d}

    response = requests.post(url + "/echo/image", params=params , files={"file": ("frame.rgb", frame)})

    img_data = response.content
    img_array = np.frombuffer(img_data, np.uint8)
    img = img_array.reshape((h, w, d)).copy()
  else:
    totext = True # echo image from fastapi server
    if totext:
      rgb = True  # use orginal image or compress to jpg
      hex = True  # use base64 or hex
      if rgb:
        if hex:
          encoded_string = bytes(frame).hex()
        else:
          encoded_string = str(base64.b64encode(frame))[2:-1]
      else:
        img_encode = cv2.imencode('.jpg', frame)[1]
        encoded_string = str(base64.b64encode(img_encode))[2:-1]

      payload ={"id": id, "w": w, "h": h, "d": d, "frame": encoded_string}

      resp = requests.post(url + "/echo/string", json=payload)
      encoded_string = resp.json()["data"]["frame"]

      if hex:
        img_array = np.frombuffer(bytes.fromhex(encoded_string), np.uint8)
      else:
        img_data = base64.b64decode(encoded_string)
        img_array = np.fromstring(img_data, np.uint8)

      if rgb:
        img = img_array.reshape((h, w, d)).copy()
      else:
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    else:
      # img_encode = cv2.imencode('.jpg', frame)[1]
      # img = cv2.imdecode(img_encode, cv2.IMREAD_COLOR)
      img = frame.copy()

  # converting the fps into integer 
  fps = np.mean(frame_drop_time)
  fps = str('{:.1f}'.format(fps) )  
  # converting the fps to string so that we can display it on frame 
  # by using putText function 
  fps = str('fps:'+ fps)
  cv2.putText(img, fps, (20, 80), font, 1, (100, 255, 0), 2, cv2.LINE_AA)
  
  cv2.imshow('video - press q to quit', img)

  if cv2.waitKey(1) == ord('q'):
      break


# 完成所有操作后，释放捕获器
cap.release()

cv2.destroyAllWindows()