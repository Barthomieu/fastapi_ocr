import pytesseract
import os
import io
import shutil
from PIL import Image
from numpy import asarray, ndarray
from fastapi import UploadFile
from .image_preprocesing import denoise_img, blur_img, convert_to_grayscale, resize_img


# pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

async def read_image(img_path, lang='eng'):
    """
    Performs OCR on a single image
    :img_path: str, path to the image file
    :lang: str, language to be used while conversion (optional, default is english)
    Returns
    :text: str, converted text from image
    """

    try:
        return pytesseract.image_to_string(img_path, lang=lang)
    except:
        return "[ERROR] Unable to process file: {0}".format(img_path)


def read_images_from_dir(dir_path, lang='eng', write_to_file=False):
    """
    Performs OCR on all images present in a directory
    :dir_path: str, path to the directory of images
    :lang: str, language to be used while conversion (optional, default is english)
    Returns
    :converted_text: dict, mapping of filename to converted text for each image
    """

    converted_text = {}
    for file_ in os.listdir(dir_path):
        if file_.endswith(('png', 'jpeg', 'jpg')):
            text = read_image(os.path.join(dir_path, file_), lang=lang)
            converted_text[os.path.join(dir_path, file_)] = text
    if write_to_file:
        for file_path, text in converted_text.items():
            _write_to_file(text, os.path.splitext(file_path)[0] + ".txt")
    return converted_text


def save_file(uploaded_file, path=".", save_as="default"):
    extension = os.path.splitext(uploaded_file.filename)[-1]
    temp_file = os.path.join(path, save_as + extension)
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    return temp_file


def _write_to_file(text, file_path):
    """
    Helper method to write text to a file
    """
    print("[INFO] Writing text to file: {0}".format(file_path))
    with open(file_path, 'w') as fp:
        fp.write(text)


async def read_img(img: UploadFile, read_exception):
    # Convert file into a byte stream
    byte_string = io.BytesIO(await img.read())

    # Validate image by attempting to open it with PIL
    try:
        img = Image.open(byte_string)
    except:
        raise read_exception

    # Convert to numpy array for opencv
    img_array = asarray(img)
    print("obraz po przetworzeniu", img_array)
    return img_array


def apply_ocr(img_array: ndarray):
    # Image processing for better predictions

    # 1. Resize image to 300 dpi
    img = resize_img(img_array)

    # 2. Convert image to grayscale
    img = convert_to_grayscale(img)

    # 3. Remove noise
    img = denoise_img(img)

    # 4. Blur & segment image
    img = blur_img(img)

    try:
        preds: str = pytesseract.image_to_string(img)
        return preds
    except:
        return "[ERROR] Unable to process file)"
