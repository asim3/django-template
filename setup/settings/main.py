from pathlib import Path
from django.urls import reverse_lazy

from .base import *
from .third_party.rest_framework import *

import os


BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# DEBUG = os.getenv('DJANGO_DEBUG', False) in (True, 'True')

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(',')

INSTALLED_APPS += [
    'user',
    'home',
    'rest_framework',
    'rest_framework_simplejwt',
    'captcha',
    'utilities',
]

MIDDLEWARE.insert(2, 'django.middleware.locale.LocaleMiddleware')

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

LOGIN_URL = reverse_lazy('admin:login')

LOGIN_REDIRECT_URL = reverse_lazy('admin:index')

LOGOUT_REDIRECT_URL = reverse_lazy('admin:login')

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'static'

STATICFILES_DIRS = [BASE_DIR / 'static_resources']

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

LOCALE_PATHS = (
    BASE_DIR / 'locale',
)

# Languages
LANGUAGE_CODE = 'ar'

LANGUAGES = [
    ('ar', 'العربية'),
    ('en', 'English'),
]

# Date & Time
TIME_ZONE = 'Asia/Riyadh'

DATE_FORMAT = 'Y / m / d'

DATETIME_FORMAT = 'Y / m / d P'

# EMAIL
DEFAULT_FROM_EMAIL = "info@gmail.com"

EMAIL_HOST = "smtp.gmail.com"

EMAIL_HOST_USER = "info@gmail.com"

EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_TIMEOUT = 15

# OTP
OTP_MAX_LENGTH = 4

OTP_DEFAULT_AGE = 60 * 5

SMS_BASE_URL = "https://api.taqnyat.sa/v1/messages"

SMS_TOKEN = "******"

SMS_DEFAULT_FROM = "django"
