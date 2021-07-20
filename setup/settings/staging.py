from .main import *
from .django_storages import *


DEBUG = True

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_CONTENT_TYPE_NOSNIFF = True

# for older browsers
SECURE_BROWSER_XSS_FILTER = True

SECURE_REFERRER_POLICY = 'same-origin'
