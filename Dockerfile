
FROM python:3.9-slim

COPY ./requirements.txt /requirements.txt
COPY ./app /app

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        python3-dev \
        python3-setuptools \
        tesseract-ocr \
        libgl1 \
        make \
        gcc \
    && python3 -m pip install -r requirements.txt


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
