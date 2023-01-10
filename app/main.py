import os
import shutil
import uvicorn
import app.utils.image_ocr as ocr
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/extract_text")
async def perform_ocr(image: UploadFile = File(...)):
    temp_file = _save_file_to_disc(image, path="app/temp", save_as="temp")
    text = await ocr.read_image(temp_file)
    return {"filename": image.filename, "text": text}

def _save_file_to_disc(uploaded_file, path=".", save_as="default"):
    extension = os.path.splitext(uploaded_file.filename)[-1]
    temp_file = os.path.join(path, save_as + extension)
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    return temp_file


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)