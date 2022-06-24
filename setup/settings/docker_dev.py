import dj_database_url

from .main import *


DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

MAX_CONN_AGE = 600

# Ensure STATIC_ROOT exists.
# os.makedirs(STATIC_ROOT, exist_ok=True)

DATABASES = {
    "default": dj_database_url.config(conn_max_age=MAX_CONN_AGE)
}

CAPTCHA_TEST_MODE = True

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
