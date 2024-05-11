from .main import *


DEBUG = False

ALLOWED_HOSTS = [
    "0.0.0.0",
    "127.0.0.1",
    "localhost",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MIDDLEWARE.insert(2, 'debug_toolbar.middleware.DebugToolbarMiddleware')

CAPTCHA_TEST_MODE = True

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

INTERNAL_IPS = ["127.0.0.1"]
