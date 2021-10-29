FROM python:3.8-alpine3.12

ADD __app_name__/requirements.txt /app/requirements.txt

RUN set -ex \
    && apk add --no-cache --virtual .build-deps postgresql-dev build-base \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /app/requirements.txt \
    && runDeps="$(scanelf --needed --nobanner --recursive /env \
    | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
    | sort -u \
    | xargs -r apk info --installed \
    | sort -u)" \
    && apk add --virtual rundeps $runDeps \
    && apk del .build-deps


# setup python virtual environment
ENV VIRTUAL_ENV /__app_name__/env
ENV PATH /env/bin:$PATH

RUN adduser -D myuser
USER myuser

ADD __app_name__ /app
WORKDIR /app

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "__app_name__.wsgi"]