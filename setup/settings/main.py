from pathlib import Path

from .base import *

import os


BASE_DIR = Path(__file__).resolve().parent.parent.parent


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')


DEBUG = os.getenv('DJANGO_DEBUG', False) in (True, 'True')


ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(',')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
