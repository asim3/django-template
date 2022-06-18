from .main import *


DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

CAPTCHA_TEST_MODE = True

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
