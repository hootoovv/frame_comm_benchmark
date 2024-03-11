import zmq
import cv2
import numpy as np
import time
import platform

from multiprocessing import shared_memory

shd_frame = None

def connect(address, context):
  #  Socket to talk to server
  print("Connecting to server...")
  socket = context.socket(zmq.REQ)
  socket.connect(address)
  return socket

def one_frame(socket, img, id):
  global shd_frame
  h, w, d = img.shape[:3]

  frame_size = w*h*d

  if shd_frame == None:
    shd_frame = shared_memory.SharedMemory(create=True, size=frame_size)

  buffer = shd_frame.buf
  buffer[:] = img.reshape(-1)[:]
  
  socket.send_json({"id": id, "w": w, "h": h, "d": d, "name": shd_frame.name})
  json = socket.recv_json()
  json = {"id": id, "w": w, "h": h, "d": d}

  img_array = np.frombuffer(buffer, dtype=np.uint8)
  img_decode = img_array.reshape((h, w, d))
  
  return json, img_decode.copy()

def test_image(socket):
  img = cv2.imread('data/2.jpg')

  json, frame = one_frame(socket, img, 1)

  cv2.imshow('zmq', frame)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

def test_video(socket):
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

    json, img = one_frame(socket, frame, id)

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
    address = "ipc:///tmp/zmq.sock"
  else:
    address = "tcp://127.0.0.1:5555"

  context = zmq.Context()

  socket = connect(address, context)

  # test_image(socket)

  test_video(socket)
