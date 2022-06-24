#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z postgres-compose 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

python manage.py makemigrations \
  && python manage.py migrate \
  && python manage.py collectstatic --noinput

python manage.py runserver 0.0.0.0:8000

# gunicorn --bind :8000 --workers 3 my_project_name.wsgi
