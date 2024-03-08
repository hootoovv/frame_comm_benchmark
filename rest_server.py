from fastapi import FastAPI, UploadFile, Response, File
from fastapi.responses import StreamingResponse
import uvicorn
import io
import json
import http
import platform
import os

app = FastAPI()

@app.get("/")
async def root():
  return {"message": "FastAPI Server"}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
  file_bytes = file.file.read()
  file_name = "upload/" + file.filename

  with open(file_name, "wb") as f:
     f.write(file_bytes)

  return {"data": {"filename": file_name, "content_type": file.content_type}}
  
@app.post("/upload/stream")  
async def upload_stream(file: bytes = File("/upload")):
    with open("upload/stream.jpg", "wb") as f:  
        f.write(file)  
    return {"file_size": len(file)}

@app.get("/download")
async def download(response: Response):
    filename = "data/1.jpg"
    with open(filename, "rb") as f:
        content = f.read()
        response.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
        response.body = content
        response.status_code = http.HTTPStatus.OK
        return response
    
@app.get("/download/stream")
async def download_stream():
    filename = "data/1.jpg"
    with open(filename, "rb") as f:
        content = f.read()

    return StreamingResponse(io.BytesIO(content), media_type="image/bmp")    

@app.post("/echo/string")
async def echo_string(data: dict):
  return {"data": data}

@app.post("/echo/image")
async def echo_image(id: int, w: int, h: int, d: int, file: UploadFile = File(...)):
    content = file.file.read()
    result = {"size": len(content), "id": id, "w": w, "h": h, "d": d}
    return StreamingResponse(io.BytesIO(content), media_type="image/raw", headers={"Additional-Info": json.dumps(result)})

# uvicorn server:app --reload
# uvicorn server:app --uds /tmp/fastapi.sock

if __name__ == '__main__':
  
  if not os.path.exists('upload'):
    os.makedirs('upload')

  sys = platform.system()
  if sys == "Linux":
    uvicorn.run(app=app, uds="/tmp/fastapi.sock")
  else:
    uvicorn.run(app=app, host="127.0.0.1", port=8000)