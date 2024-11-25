import requests
from app.logger import log_decorator
from settings.celery_settings import celery_app
from settings.config import URL_FOR_REQUEST


@log_decorator
@celery_app.task()
def get_file():
    response = requests.get(URL_FOR_REQUEST)
    files = {"file": ('1.xml', response.content, "application/xml")}

    response = requests.post(
        'http://localhost:8000/upload-xml/', files=files)
