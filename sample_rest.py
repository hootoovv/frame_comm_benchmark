import requests
import requests_unixsocket
import platform
import os

upload_source = "data/1.jpg"
# upload_source = "data/2.jpg"

sys = platform.system()
if sys == "Linux":
  url = 'http+unix://%2Ftmp%2Ffastapi.sock'
else:
  url = "http://127.0.0.1:8000"

requests_unixsocket.monkeypatch()

def test_root():
  response = requests.get(url)
  print(response.json())  

def test_download(route = "/download", local="data/download.jpg"):
  response = requests.get(url + route)

  streaming = False

  with open(local, "wb") as f:
    if streaming:
      for chunk in response.iter_content(chunk_size=4096):
        f.write(chunk)
    else:
      f.write(response.content)

def test_upload(route = "/upload", local = "data/1.jpg", remote = "upload.jpg"):
  with open(local, "rb") as f:
    content = f.read()

  response = requests.post(url + route, files={"file": (remote, content, "image/raw")})

  print(response.json())

def test_echo_string(route = "/echo/string"):
  id = 1
  w = 20
  h = 20
  d = 3
  frame = "base64str"

  payload = {"id": id, "w": w, "h": h, "d": d, "frame": frame}

  response = requests.post(url + route, json=payload)

  print(response.json()["data"])


def test_echo_image(route = "/echo/image", local_src = "data/1.jpg", local_dst = "download/echo_client_out.jpg"):
  id = 1
  w = 20
  h = 20
  d = 3

  params  = {"id": id, "w": w, "h": h, "d": d}

  with open(local_src, "rb") as fin:
    content = fin.read()

  response = requests.post(url + route, params=params , files={"file": ("frame.rgb", content, "image/raw")})

  json = response.headers.get("Additional-Info")
  print(json)

  with open(local_dst, "wb") as fout:
    fout.write(response.content)

if __name__ == '__main__':
  print("Test Home")
  test_root()
  print("OK\n")

  if not os.path.exists('download'):
    os.makedirs('download')

  print("Test Download")
  test_download("/download", "download/download.jpg")
  print("OK\n")

  print("Test Download - stream")
  test_download("/download/stream", "download/stream.jpg")
  print("OK\n")

  print("Test Upload")
  test_upload("/upload", upload_source, "upload.jpg")
  print("OK\n")

  print("Test Upload - stream")
  test_upload("/upload/stream", upload_source, "stream.jpg")
  print("OK\n")

  print("Test Echo String")
  test_echo_string("/echo/string")
  print("OK\n")

  print("Test Echo Image")
  test_echo_image("/echo/image", upload_source, "download/echo_output.jpg")
  print("OK\n")


