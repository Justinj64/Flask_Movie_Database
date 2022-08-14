FROM python:3.10-slim-bullseye
COPY ./flask_app/requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY ./flask_app/ /home/flask_app/
WORKDIR /home/flask_app/
ENV ENV=development
ENV PYTHONUNBUFFERED=True 
CMD gunicorn -b 0.0.0.0:5000 --log-file info.log --capture-output -w 4 --threads 100 main:app
