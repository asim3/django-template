#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $SQL_HOST $SQL_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

python manage.py makemigrations \
  && python manage.py migrate \
  && python manage.py collectstatic --noinput

python manage.py runserver 0.0.0.0:8000

# gunicorn --bind :8000 --workers 3 my_project_name.wsgi
