import PIL

import app.utils.image_ocr as ocr
import pytesseract
from PIL import Image
from app.utils.image_preprocesing import preprocess_image
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

from os.path import exists


path = r'../temp/ocrTest3.jpg'
print(exists(path))


image = preprocess_image(path)

text = ocr.read_image(path)
print(text)


def process_image(image):
    return pytesseract.image_to_string(image)


image = PIL.Image.open(path)
text1 = process_image(image)
print(text1)