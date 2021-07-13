from pathlib import Path
from django.urls import reverse_lazy

from .base import *

import os


BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# DEBUG = os.getenv('DJANGO_DEBUG', False) in (True, 'True')

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(',')

INSTALLED_APPS += [
    'crispy_forms',
    'simple_history',
]

TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'static'

STATICFILES_DIRS = [BASE_DIR / 'static_resources']

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LANGUAGE_CODE = 'ar-sa'

# LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('ar', 'العربية'),
    ('en', 'English'),
]

LOCALE_PATHS = (
    BASE_DIR / 'locale',
)

TIME_ZONE = 'Asia/Riyadh'

LOGIN_URL = reverse_lazy('admin:login')

LOGIN_REDIRECT_URL = reverse_lazy('admin:index')

LOGOUT_REDIRECT_URL = reverse_lazy('admin:login')
