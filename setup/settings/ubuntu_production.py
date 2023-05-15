import dj_database_url

from .main import *


DEBUG = False

ALLOWED_HOSTS = [
    "asim.sa",
    "asim.com",
]

MAX_CONN_AGE = 600

DATABASES = {
    "default": dj_database_url.config(conn_max_age=MAX_CONN_AGE)
}

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
