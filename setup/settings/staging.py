from .main import *
from .third_party.django_storages import *
from .third_party.heroku import *


DEBUG = False

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_HTTPONLY = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_CONTENT_TYPE_NOSNIFF = True

# for older browsers
SECURE_BROWSER_XSS_FILTER = True

SECURE_REFERRER_POLICY = 'same-origin'

# session age = 20 minutes
SESSION_COOKIE_AGE = 60 * 20

AWS_LOCATION = 'staging'
