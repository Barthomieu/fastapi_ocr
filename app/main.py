import shutil
import uvicorn
import base64
from utils.image_ocr import *
from fastapi import FastAPI, Request, UploadFile, File, Depends, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/extract_text")
async def perform_ocr(image: UploadFile = File(...)):
    temp_file = _save_file_to_disc(image, path="app/temp", save_as="temp")
    text = await read_image(temp_file)
    try:
        contents = image.file.read()
        with open("uploaded_" + image.filename, "wb") as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        image.file.close()

    base64_encoded_image = base64.b64encode(contents).decode("utf-8")
    return {"filename": image.filename, "text": text, "myImage": base64_encoded_image}

@app.post("/convert")
async def post_image_to_text(file: UploadFile = File(...)):
    img = await read_img(file, HTTPException(status_code=422, detail="Invalid image"))

    ocr_predictions: str = apply_ocr(img)
    print(ocr_predictions)
    return {
        "results": {
            "raw": ocr_predictions,
            "cleaned": ocr_predictions.replace("\n", " ").strip(),
            "lines": ocr_predictions.split("\n"),
        }
    }


def _save_file_to_disc(uploaded_file, path=".", save_as="default"):
    extension = os.path.splitext(uploaded_file.filename)[-1]
    temp_file = os.path.join(path, save_as + extension)
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    return temp_file


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)