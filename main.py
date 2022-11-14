import os.path
import shutil
import uvicorn
import utils.image_ocr as ocr
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.params import File
from fastapi.templating import Jinja2Templates
app = FastAPI()

templates = Jinja2Templates(directory="templates")

#@app.get("/")
#async def root():
#    return {"message": "Hello World"}

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/get_text")
def preform_ocr(image: UploadFile = File(...)):
    temp_file = _save_file_to_disc(image, path="temp", save_as="temp")
    text = ocr.read_image(temp_file)
    return {"filename": image.filenamee, "text": text}

def _save_file_to_disc(uploaded_file, path=".", save_as="default"):
    extension = os.path.splitext(uploaded_file.filename)[-1]
    temp_file = os.path.json(path, save_as + extension)
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(uploaded_file, buffer)
    return temp_file


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)