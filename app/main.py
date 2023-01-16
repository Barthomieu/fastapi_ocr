import os
import shutil
import uvicorn
import base64
import asyncio
import time
import app.utils.image_ocr as ocr
from typing import List
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
    temp_file = save_file(image, path="app/temp", save_as="temp")
    text = await ocr.read_image(temp_file)
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

@app.post("/extract_text_from_many_files")
async def extract_text(Images: List[UploadFile] = File(...)):
    response = {}
    s = time.time()
    tasks = []
    for img in Images:
        print("Images Uploaded: ", img.filename)
        temp_file = save_file(img, path="./", save_as=img.filename)
        tasks.append(asyncio.create_task(ocr.read_image(temp_file)))
    text = await asyncio.gather(*tasks)
    for i in range(len(text)):
        response[Images[i].filename] = text[i]
    response["Time Taken"] = round((time.time() - s),2)

    return response


@app.post("/convert")
async def post_image_to_text(file: UploadFile = File(...)):
    img = await ocr.read_img(file, HTTPException(status_code=422, detail="Invalid image"))

    ocr_predictions: str = ocr.apply_ocr(img)
    print(ocr_predictions)
    return {
        "results": {
            "raw": ocr_predictions,
            "cleaned": ocr_predictions.replace("\n", " ").strip(),
            "lines": ocr_predictions.split("\n"),
        }
    }


def save_file(uploaded_file, path=".", save_as="default"):
    extension = os.path.splitext(uploaded_file.filename)[-1]
    temp_file = os.path.join(path, save_as + extension)
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    return temp_file


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)