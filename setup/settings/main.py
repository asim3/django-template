from pathlib import Path

from .base import *

import os


BASE_DIR = Path(__file__).resolve().parent.parent.parent


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')


# DEBUG = os.getenv('DJANGO_DEBUG', False) in (True, 'True')


ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(',')


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


SECURE_SSL_REDIRECT = True


SESSION_COOKIE_SECURE = True


CSRF_COOKIE_SECURE = True


SECURE_CONTENT_TYPE_NOSNIFF = True


# for older browsers
SECURE_BROWSER_XSS_FILTER = True


SECURE_REFERRER_POLICY = 'same-origin'
