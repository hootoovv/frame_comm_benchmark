import time
import zmq
import signal
import sys
import platform

if __name__ == '__main__':
  context = zmq.Context()
  socket = context.socket(zmq.REP)

  sys = platform.system()
  if sys == "Linux":
    socket.bind("ipc:///tmp/zmq.sock")
  else:
    socket.bind("tcp://127.0.0.1:5555")

  print("Server started.")

  while True:
    json = socket.recv_json()
    socket.send_json(json)

    # time.sleep(1)
    frame = socket.recv()
    socket.send(frame)

    # print(json)
