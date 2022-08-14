import os
from celery import Celery
from config import get_config

# If no `env` is specified, we consider the `development` config by default
CONFIG = get_config(os.getenv("ENV", "development"))
BROKER_URL = CONFIG.get("RABBITMQ_BROKER_URL")
print({"CONFIG": CONFIG})

# Celery App and Task Definitions:
app = Celery('db_worker', broker=BROKER_URL)

'''
    worker_prefetch_multiplier : The prefetch limit is a limit for the
    number of tasks (messages) a worker can reserve for itself
    limit = multiplier * number of processes

    task_acks_late : If set to True, messages for this task will be
    acknowledged after the task has been executed, not just before
'''
app.conf.update({
    "worker_prefetch_multiplier": 1,
    "task_acks_late": True
})
