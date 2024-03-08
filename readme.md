# Benchmark of vidoe frame transmission via RestServer, gRPC and ZMQ

## RestServer

### 1. Description

use FastAPI to build up a HTTP restful server. try followings:

1. baseline: not go through different process, decode and draw frame in same process.
2. file upload and download: use http multipart file upload and download. all frame data go through RAM not read/write Harddisk.
3. frame rgb data encode and decode: convert to base64 string. post the string to server, echo back then decode and draw frame.
4. frame jpg encode and decode: use jpeg encode and decode then convert to base64 string. wiht jpeg compress and decompress which will consume CPU, but data size is much less than rgb.

### 2. Benchmark

```shell
pip install -r requirements_rest.txt

# start rest api server (fastapi)
python rest_server.py

# create anothor terminal and run rest client
# need desktop support, cv windows will pop up and show frame rate
pyhthon rest_client.py
```

manual change following variable in code to test different branch of rest_client.py

```python
upload = True # test file upload and download
totext = False # baseline, direct draw frame
totext = True # echo image from fastapi server
rgb = True  # use orginal rgb frame or compress to jpg
```

## gRPC

### 1. Description

use gRPC to send frame between server and client.

### 2. Benchmark

```shell
pip install -r requirements_grpc.txt

# generate python source file from proto file
python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. ./protobuf/api.proto

# start rest api server (fastapi)
python grpc_server.py

# create anothor terminal and run rest client
# need desktop support, cv windows will pop up and show frame rate
pyhthon grpc_client.py

```

## ZMQ

### 1. Description

use ZMQ to send frame between server and client.

### 2. Benchmark

```shell
pip install -r requirements_zmq.txt

# start zmq server (ipc on linux, localhost on windows)
python zmq_server.py

# create anothor terminal and run zmq client
pyhthon zmq_client.py
```

## Result

* baseline: 105 fps
* zmq: 50 fps
* gRPC: 25 fps
* base64 encode and decode: 4.8 fps
* jpeg encode and decode: 8.2 fps
* file upload and download: 3.5 fps

## Conclusion

1. zmq is the fastest way, it just use socket to send binary data. (via Unix Domain Socket). but you need process the data structure yourself.
2. gRPC is much faster than RestServer. gPRC go through binary data transfer and HTTP is going through string transfer. multipart upload will convert to base64?
3. python buildin base64 is super slow. pybase64 is a little faster. both is slow, should try a C implementation base64 module. maybe due to python cannot run on multi core well.
4. go jpeg compress then base64 is faster than orgianl rgb to base64. should due to less data need to convert to base64, though the image quality will drop due to jpeg compress.
5. http upload and download is slower even than base64 encode and decode.
6. with huge data trasmission, localhost (via virtual network driver) and uds (Unix Domain Socket, which not going through network stack) don't have too much different. small packet and much requent data transmission should see the difference.
7. none of above method is good enough for video transmission.
