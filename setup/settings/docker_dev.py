from dotenv import dotenv_values

from .main import *


DOTENV_CONFIG = dotenv_values(".env")

DEBUG = True

ALLOWED_HOSTS = [
    "0.0.0.0",
    "127.0.0.1",
    "localhost",
    "*",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "postgresql",
        "PORT": "5432",
        "NAME": "db_pg",
        "USER": "user_pg",
        "PASSWORD": DOTENV_CONFIG.get('POSTGRES_PASSWORD'),
    }
}

INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE.insert(2, 'debug_toolbar.middleware.DebugToolbarMiddleware')

CAPTCHA_TEST_MODE = True

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

INTERNAL_IPS = ["127.0.0.1"]
