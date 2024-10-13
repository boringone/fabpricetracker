#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"
echo "Apply database migrations"
python manage.py migrate
echo "Collecting static files"
python manage.py collectstatic
echo "Starting server"
gunicorn fabpricetracker.wsgi --bind 0.0.0.0:8000
