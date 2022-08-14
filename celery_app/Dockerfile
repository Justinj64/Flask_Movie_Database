FROM python:3.10-slim-bullseye
COPY ./src/requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY ./src/ /home/src/
WORKDIR /home/src/
ENV ENV=development
CMD celery -A scripts.consumer worker -l=info --logfile=worker.log --concurrency 50 -Q DB_OPERATIONS
