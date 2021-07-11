from pathlib import Path

from .base import *

import os


BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# DEBUG = os.getenv('DJANGO_DEBUG', False) in (True, 'True')

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(',')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'static'

STATICFILES_DIRS = [BASE_DIR / 'static_resources']

MEDIA_URL = '/media/'

MEDIA_ROOT = [BASE_DIR / 'media']

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LANGUAGE_CODE = 'ar-sa'

# LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('ar', 'العربية'),
    ('en', 'English'),
]

LOCALE_PATHS = (
    (BASE_DIR / 'locale'),
)
