import requests
from app.logger import log_decorator
from settings.celery_settings import celery_app


@log_decorator
@celery_app.task()
def get_file():
    response = requests.get('http://localhost:5000/get/')
    files = {"file": ('1.xml', response.content, "application/xml")}

    response = requests.post(
        'http://localhost:8000/upload-xml/', files=files)
