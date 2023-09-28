from .main import *

import dj_database_url


ALLOWED_HOSTS = [
    "0.0.0.0",
    "127.0.0.1",
    "localhost",
    "my_project_name.asim.sa",
    "123.456.789.123",
]

DATABASES = {
    "default": dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
    )
}

CAPTCHA_TEST_MODE = True

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
