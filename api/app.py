from zipfile import ZipFile
import io
from api.bin.filters import apply_filter
from typing import List
from fastapi import FastAPI, File, UploadFile, Request, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse


app = FastAPI()

filters_available = [
    "blur",
    "contour",
    "detail",
    "edge_enhance",
    "edge_enhance_more",
    "emboss",
    "find_edges",
    "sharpen",
    "smooth",
    "smooth_more",
]


@app.api_route("/", methods=["GET", "POST"])
async def index():
  response = {
      "filters_available": filters_available,
      "usage": {"http_method": "POST", "URL": "/<filter_available>/"},
  }
  
  return jsonable_encoder(response)


@app.post("/{filter}")
async def image_filter(filter: str, images: List[UploadFile] = File(...)):
  if filter not in filters_available:
    response = {"error": "incorrect filter"}
    return jsonable_encoder(response)

  buffer = io.BytesIO()
  zipObject = ZipFile(buffer, mode="w")

  for image in images:
    filtered_image = await apply_filter(image.file, filter)
    zipObject.writestr(image.filename, filtered_image.read())

  zipObject.close()

  buffer.seek(0)
  response = StreamingResponse(buffer, media_type="application/zip")
  response.headers["Content-Disposition"] = "attachment; filename=images.zip"

  return response
