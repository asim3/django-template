import dj_database_url


MAX_CONN_AGE = 600

# Ensure STATIC_ROOT exists.
# os.makedirs(STATIC_ROOT, exist_ok=True)

DATABASES = {
    'default': dj_database_url.config(conn_max_age=MAX_CONN_AGE, ssl_require=True)
}
