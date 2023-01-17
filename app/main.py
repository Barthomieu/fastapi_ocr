import os
import io
import cv2
import uvicorn
import base64
import asyncio
import time
import requests
import pytesseract
import app.utils.image_ocr as ocr
import app.utils.image_preprocesing as preprocesing
from typing import List
from PIL import Image
from fastapi import FastAPI, Request, UploadFile, File, Depends, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/extract_text")
async def perform_ocr(image: UploadFile = File(...)):
    temp_file = ocr.save_file(image, path="app/temp", save_as="temp")
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
        temp_file = ocr.save_file(img, path="./", save_as=img.filename)
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


@app.post("/extract_text_from_url")
async def extract_text_from_url(url: str):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=422, detail="Invalid image URL")
        image = Image.open(io.BytesIO(response.content))
        text = pytesseract.image_to_string(image)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@app.post("/extract_text_with_language")
async def extract_text_with_language(image: UploadFile = File(...), language: str = "eng"):
    temp_file = ocr.save_file(image, path="app/temp", save_as="temp")
    image = Image.open(temp_file)
    text = pytesseract.image_to_string(image, lang=language)
    return {"text": text}

@app.post("/search_text_in_images/{text_to_search}")
async def search_text_in_images(text_to_search: str, images: List[UploadFile] = File(...)):
    tasks = []
    for img in images:
        temp_file = ocr.save_file(img, path="app/temp", save_as=img.filename)
        tasks.append(asyncio.create_task(ocr.read_image(temp_file)))
    texts = await asyncio.gather(*tasks)
    for i in range(len(texts)):
        if text_to_search in texts[i]:
            return {"status": "found", "text": text_to_search, "file_name": images[i].filename}
    return {"status": "not found", "text": text_to_search}

@app.post("/get_image_with_bounding_boxes")
async def post_image_with_bounding_boxes(image: UploadFile = File(...)):
    temp_file = ocr.save_file(image, path="app/temp", save_as="temp")
    img = preprocesing.get_image_with_bounding_boxes(temp_file)
    img_pil = Image.fromarray(img)
    # Save the image to a BytesIO object
    img_bytes = io.BytesIO()
    img_pil.save(img_bytes, format='JPEG')
    # Set the pointer to the beginning of the BytesIO object
    img_bytes.seek(0)
    return StreamingResponse(img_bytes, media_type='image/jpeg')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)