import PIL

import app.utils.image_ocr as ocr
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
path = 'temp.png'

text = ocr.read_image(path)
print(text)


def process_image(image):
    return pytesseract.image_to_string(image)


image = PIL.Image.open('temp.png')
text1 = process_image(image)
print(text1)