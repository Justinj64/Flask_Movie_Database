import os
from celery import Celery
from config import get_config

CONFIG = get_config(os.getenv("ENV", "development"))
BROKER_URL = CONFIG.get("RABBITMQ_BROKER_URL")
print({"CONFIG": CONFIG})

app = Celery('db_worker', broker=BROKER_URL,)

app.conf.update({
    "worker_prefetch_multiplier": 1,
    "task_acks_late": True
})


