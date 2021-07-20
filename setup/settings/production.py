from .main import *
from .django_storages import *


DEBUG = False

SECURE_SSL_REDIRECT = True

SECURE_HSTS_SECONDS = 3600

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_CONTENT_TYPE_NOSNIFF = True

# for older browsers
SECURE_BROWSER_XSS_FILTER = True

SECURE_REFERRER_POLICY = 'same-origin'

# django_storages
AWS_STORAGE_BUCKET_NAME = 'project-production'
