
from celery import Celery
from settings.config import REDIS_HOST


celery_app = Celery(__name__, broker=f'redis://{REDIS_HOST}:6379/0',
                    backend=f'redis://{REDIS_HOST}:6379/0')
celery_app.conf.timezone = "UTC"
celery_app.conf.beat_max_loop_interval = 1
celery_app.conf.update(include=["app.tasks"])
celery_app.conf.beat_schedule = {
    "add-every-day": {
        "task": "app.tasks.get_file",
        "schedule": 86400
    }
}
