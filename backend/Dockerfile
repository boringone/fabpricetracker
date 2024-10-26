FROM python:3.11-slim-buster
EXPOSE 8000
WORKDIR /app
# copy all command scripts
COPY entrypoint.sh /web_start
COPY ./celery_beat/start.sh /celery_beat_start
COPY ./flower/start.sh /flower_start
COPY ./celery/start.sh /celery_start

COPY requirements.txt /app/
RUN apt-get update && apt-get -y install libpq-dev gcc netcat-openbsd redis-server --fix-missing && pip install psycopg2
RUN apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
RUN pip3 install -r requirements.txt --no-cache-dir


COPY . /app/
