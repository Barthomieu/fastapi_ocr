import PIL
import app.utils.image_ocr as ocr
from os.path import exists
from PIL import Image
from app.utils.image_preprocesing import *

# pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

path = r'../temp/ocrTest3.jpg'
print(exists(path))

text = ocr.read_image(path)
print(text)


def process_image(image1):
    return pytesseract.image_to_string(image1)


image = PIL.Image.open(path)
text1 = process_image(image)
print(text1)
