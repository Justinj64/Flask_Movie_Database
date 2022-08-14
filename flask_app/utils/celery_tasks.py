from celery import Celery
import os
from config import get_config

# If no `env` is specified, we consider the `development` config by default
env_config = os.getenv("ENV", "development")
conf = get_config(env_config)

# Celery App and Task Definitions:
celery_app = Celery(broker=conf.get('RABBITMQ_BROKER_URL'))


'''
    Created 3 tasks to handle insert, update and deletion of records
    Task is referenced here but the actual processing is done in
    /scripts/consumer.py in the celery_app module
'''


@celery_app.task(name="db_worker:insert_record")
def insert_record(data):
    pass


@celery_app.task(name="db_worker:update_record")
def update_record(data):
    pass


@celery_app.task(name="db_worker:delete_record")
def delete_record(data):
    pass