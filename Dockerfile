#FROM python:3.9
#WORKDIR /code
#COPY ./requirements.txt /code/requirements.txt
#RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
#COPY ./app /code/app

FROM python:3.9-slim

COPY ./requirements.txt /requirements.txt
COPY ./app /app

#RUN apt-get update
#RUN apt install -y libgl1-mesa-glx
#RUN apt-get install -y tesseract-ocr-all

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        python3-dev \
        python3-setuptools \
        tesseract-ocr \
        make \
        gcc \
    && python3 -m pip install -r requirements.txt


#RUN pip install -r /requirements.txt


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
