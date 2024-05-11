from dotenv import dotenv_values

from .main import *


DOTENV_CONFIG = dotenv_values(".env")

DEBUG = DOTENV_CONFIG.get("DJANGO_DEBUG") in (True, "True")

ALLOWED_HOSTS = [
    "0.0.0.0",
    "127.0.0.1",
    "localhost",
    "my_project_name.asimt.sa",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "postgresql-stag",
        "PORT": "5432",
        "NAME": "my_project_name_db_v4",
        "USER": "my_project_name_user_v4",
        "PASSWORD": DOTENV_CONFIG.get('POSTGRES_PASSWORD'),
    }
}

STATIC_URL = "https://my_project_name.static.asimt.sa/static/"

MEDIA_URL = "https://my_project_name.static.asimt.sa/media/"

CSRF_TRUSTED_ORIGINS = [
    "https://*.asimt.sa",
    "https://notes.asimt.sa",
    "https://my_project_name.static.asimt.sa",
]

# EMAIL
SERVER_EMAIL = "my_project_name@gmail.com"

DEFAULT_FROM_EMAIL = "my_project_name@gmail.com"

EMAIL_HOST_USER = "my_project_name@gmail.com"

EMAIL_SUBJECT_PREFIX = "[my_project_name.asimt.sa]"
