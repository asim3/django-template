import django_heroku
import os


django_heroku.settings(locals())

DEFAULT_FROM_EMAIL = "info@gmail.com"

EMAIL_HOST = "smtp.gmail.com"

EMAIL_HOST_USER = "info@gmail.com"

EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_TIMEOUT = 15
