from dotenv import dotenv_values

from .main import *
# from .third_party.django_storages import *


DOTENV_CONFIG = dotenv_values(".env")

DEBUG = False

ALLOWED_HOSTS = [
    "0.0.0.0",
    "127.0.0.1",
    "localhost",
    "my_project_name.sa",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "postgresql-prod",
        "PORT": "5432",
        "NAME": "my_project_name_db_v3",
        "USER": "my_project_name_user_v3",
        "PASSWORD": DOTENV_CONFIG.get('POSTGRES_PASSWORD'),
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

STATIC_URL = "https://static.my_project_name.sa/static/"

MEDIA_URL = "https://static.my_project_name.sa/media/"

# SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = [
    "https://my_project_name.sa",
    "https://www.my_project_name.sa",
    "https://static.my_project_name.sa",
]

SECURE_CONTENT_TYPE_NOSNIFF = True

# for older browsers
SECURE_BROWSER_XSS_FILTER = True

SECURE_REFERRER_POLICY = 'same-origin'

SECURE_HSTS_SECONDS = 3600

SECURE_HSTS_PRELOAD = True

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# third_party
AWS_LOCATION = 'production'

# EMAIL
SERVER_EMAIL = "my_project_name@gmail.com"

DEFAULT_FROM_EMAIL = "my_project_name@gmail.com"

EMAIL_HOST_USER = "my_project_name@gmail.com"

EMAIL_SUBJECT_PREFIX = "[my_project_name.sa]"
