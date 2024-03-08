import grpc
from protobuf import api_pb2
from protobuf import api_pb2_grpc
import cv2
import numpy as np
import json
import time
import platform

MAX_MESSAGE_LENGTH = 4096*2160*4
 
def test_jpg(address = "127.0.0.1:5001"):
  # channel = grpc.insecure_channel(address)
  channel = grpc.insecure_channel(address)
  
  stub = api_pb2_grpc.APIStub(channel)
  
  img = cv2.imread('data/1.jpg')
  h, w, d = img.shape[:3]

  response = stub.process_frame(api_pb2.request_frame(id=1, width=w, height=h, depth=d, frame=bytes(img)))

  frame = response.frame
  json_str = response.json

  result = json.loads(json_str)

  print(result)

  img_array = np.frombuffer(frame, dtype=np.uint8)
  img_decode = img_array.reshape((h, w, d))

  cv2.imshow('result', img_decode)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
 
def test_video(address = "127.0.0.1:5001"):
  channel = grpc.insecure_channel(address, options=[
                             ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
                             ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
                         ])
  stub = api_pb2_grpc.APIStub(channel)
 
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

    # img = frame.copy()
    response = stub.process_frame(api_pb2.request_frame(id=1, width=w, height=h, depth=d, frame=bytes(frame)))

    image = response.frame
    # json_str = response.json
    # result = json.loads(json_str)
    # print(result)

    img_array = np.frombuffer(image, dtype=np.uint8)
    img = img_array.reshape((h, w, d)).copy()

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

if __name__ == '__main__':
  sys = platform.system()
  if sys == "Linux":
    address = "unix:///tmp/grpc.sock"
  else:
    address = "127.0.0.1:5001"

  test_jpg(address)
  test_video(address)