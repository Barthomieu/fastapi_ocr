## About project

----------------------------------
The project is an implementation of a microservice for reading text from images, powered by  Tesseract OCR, that can be easily incorporated in any application via a simple-to-use API built with FastAPI. The whole microservice is containerized using Docker, making it easier for anyone to set up a local copy and bend it to their needs.

The microservice also cleans and processes the uploaded images with OpenCV; improving the OCR predictions of the Tesseract model.

## Built With
- [Python](https://python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Tesseract OCR](https://tesseract-ocr.github.io/)
- [Docker](https://www.docker.com/)




## Run locally

----------------------------
### Clone the repo
```angular2html
git clone https://github.com/Barthomieu/fastapi_ocr.git
```

### Install dependencies
```
pip install -r requirements.txt
```
### Run Server
```
cd app
uvicorn pdfapi:app --host 0.0.0.0 --port 8000 --reload
```
### Run on Docker
```
docker build -t fastapi_ocr .   
```
### Run the docker container
```
docker run -d --name my_container api_ocr 
```


## Documentation

-----------------------------------------------------------
The api contains the following endpoints

* #### ```/extract_text``` - returns text from uploaded file
* #### ```/extract_text_from_many_files``` - return text from all uploades files
* #### ```/extract_text_from_url``` - return text from url with image
