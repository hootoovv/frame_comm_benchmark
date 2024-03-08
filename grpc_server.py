import grpc
import time
from concurrent import futures
from protobuf import api_pb2
from protobuf import api_pb2_grpc
import numpy as np
import json
import platform

import threading
 
MAX_MESSAGE_LENGTH = 4096*2160*4

class APIServer(api_pb2_grpc.APIServicer):
  def __init__(self):
    pass
  
  def process_frame(self, request, context):
    id = request.id
    w = request.width
    h = request.height
    d = request.depth

    frame = request.frame

    img_array = np.frombuffer(frame, dtype=np.uint8)
    img = img_array.reshape((h, w, d))

    result = self.sample_result()

    return api_pb2.response_frame(id=id, width=w, height=h, depth=d, frame=bytes(img), json=json.dumps(result))


  def sample_result(self):
    """
    推理图像帧
      
    Args:
        frame (numpy.ndarray): 图像帧
    
    Returns:
        result: 推理结果
    """
    person1 = {
      'rect': { # 人体矩形 - 人的位置
        'x': 840,
        'y': 820,
        'w': 20,
        'h': 40
      },
      'id': 0,
      'type': 'person', # 类型可以为'person', 'vehicle', 'object'。类型为person时，ext提供头盔，工装，短袖，打电话，吸烟等信息
      'name': '张三',
      'ext' : {
        'helmet': 0, # 0:无 1:有 2:未知
        'uniform': 1, # 0:无 1:有 2:未知
        'short_sleeve': 2, # 0:无 1:有 2:未知
        'phone_call': 0, # 0:无 1:有 2:未知
        'smoking': 0, # 0:无 1:有 2:未知
      },
      'last_position': {  # 上一次检测到的位置, None 表示首次出现
        'x': 801,
        'y': 821,
        'w': 20,
        'h': 40
      }
    }

    person2 = {
      'rect': { # 人体矩形 - 人的位置
        'x': 320,
        'y': 500,
        'w': 20,
        'h': 40
      },
      'id': 1,
      'type': 'person', # 类型可以为'person', 'vehicle', 'object'。
      'name': '未识别',
      'ext' : {
        'helmet': 0, # 0:无 1:有 2:未知
        'uniform': 1, # 0:无 1:有 2:未知
        'short_sleeve': 2, # 0:无 1:有 2:未知
        'phone_call': 0, # 0:无 1:有 2:未知
        'smoking': 0, # 0:无 1:有 2:未知
      },
      'last_position': None # 上一次检测到的位置, None 表示首次出现
    }

    vehicle1 = {
    'rect': {
        'x': 210,
        'y': 420,
        'w': 80,
        'h': 180
      },
      'id': 2,
      'type': 'vehicle', # 类型可以为'person', 'vehicle', 'object'。类型为vehicle时，ext提供 车速，类型，车牌等信息
      'name': '车辆',
      'ext' : {
        'speed':  '14 km/h',
        'type': '吊车',
        'plate': '冀B12345',
        'other': '黄色' # 提供任何AI能识别的可读信息
      }
    }

    object1 = {
    'rect': {
        'x': 820,
        'y': 290,
        'w': 30,
        'h': 30
      },
      'id': 3,
      'type': 'object', # 类型可以为'person', 'vehicle', 'object'。类型为object时，ext提供提供 积水，火焰，异物等信息，并在other里提供任何AI能识别目标分类信息及置信度(最多3个)
      'name': '异物', # '积水', '火焰', '异物'
      'ext': {
        'puddle':  0, # 0:无 1:有 2:未知
        'fire': 0, # 0:无 1:有 2:未知
        'object': 1, # 0:无 1:有 2:未知
        'other': [
          {
            'name': '塑料袋',
            'confidence': 0.9
          },
          {
            'name': '风筝',
            'confidence': 0.8
          },
          {
            'name': '气球',
            'confidence': 0.7
          }
        ]
      }
    }

    result = {
      'frame_id': 0,
      'objects': [person1, person2, vehicle1, object1]
    }

    return result

def serve():

  server = grpc.server(futures.ThreadPoolExecutor(max_workers=4), options=[
                            ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
                            ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
                        ])

  api_pb2_grpc.add_APIServicer_to_server(APIServer(), server)

  server.add_insecure_port('[::]:5001')

  sys = platform.system()
  if sys == "Linux":
    server.add_insecure_port("unix:///tmp/grpc.sock")

  server.start()

  print('Server Started.')

  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
      server.stop(0)
 
def main():
    #t1 = threading.Thread(target=serve)
    #t1.start()

    serve()
 
if __name__ == '__main__':
  main()