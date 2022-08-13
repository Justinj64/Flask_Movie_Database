from celery import Celery
import os
from config import get_config

# Get Config:

env_config = os.getenv("ENV", "development")
conf = get_config(env_config)

# Celery App and Task Definitions:
celery_app = Celery(broker=conf.get('RABBITMQ_BROKER_URL'))


@celery_app.task(name="db_worker:insert_record")
def insert_record(data):
    pass

@celery_app.task(name="db_worker:update_record")
def update_record(data):
    pass

@celery_app.task(name="db_worker:delete_record")
def delete_record(data):
    pass