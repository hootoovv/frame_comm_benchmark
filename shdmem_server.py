from multiprocessing import shared_memory

import zmq
import sys
import platform
import numpy as np

if __name__ == '__main__':
  context = zmq.Context()
  socket = context.socket(zmq.REP)
  shd_frame = None

  sys = platform.system()
  if sys == "Linux":
    socket.bind("ipc:///tmp/zmq.sock")
  else:
    socket.bind("tcp://127.0.0.1:5555")

  print("Server started.")

  while True:
    json = socket.recv_json()

    w = json["w"]
    h = json["h"]
    d = json["d"]
    name = json["name"]

    frame_size = w*h*d

    if shd_frame == None:
      shd_frame = shared_memory.SharedMemory(name)

    buffer = shd_frame.buf

    img_array = np.frombuffer(buffer, dtype=np.uint8)
    # img_decode = img_array.reshape((h, w, d))
    # dst = np.zeros((80, 80, 3), dtype=np.uint8)
    # img_decode[0:80, 0:80] = dst

    buffer[:] = img_array[:]

    # time.sleep(1)

    socket.send_json(json)

    # print(json)