FROM python:3.9-alpine

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1

# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .

RUN apk update && apk --no-cache add --virtual .build-dependencies \
    build-base \
    python3-dev \
    # wget dependency
    openssl \
    # psycopg2 dependencies
    postgresql-dev \
    gcc \
    musl-dev \
    # Pillow dependencies
    freetype-dev \
    fribidi-dev \
    harfbuzz-dev \
    jpeg-dev \
    lcms2-dev \
    openjpeg-dev \
    tcl-dev \
    tiff-dev \
    tk-dev \
    zlib-dev \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del --no-cache .build-dependencies \
    # install psycopg2 dependencies
    && apk add libpq


# create the app user
RUN mkdir -p /home/app
RUN addgroup -S app && adduser -S app -G app


# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME


# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x  $APP_HOME/entrypoint.sh


# copy project
COPY ./my_project_name $APP_HOME


# chown all the files to the app user
RUN chown -R app:app $APP_HOME
USER app


ENTRYPOINT ["/home/app/web/entrypoint.sh"]
