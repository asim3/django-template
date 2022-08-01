from .main import *


DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE.insert(2, 'debug_toolbar.middleware.DebugToolbarMiddleware')

CAPTCHA_TEST_MODE = True

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

INTERNAL_IPS = ["127.0.0.1"]
