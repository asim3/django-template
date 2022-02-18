FROM python:3.9-alpine

RUN apk update 

RUN apk --no-cache add \
    build-base \
    python3-dev \
    # wget dependency
    openssl \
    # psycopg2 dependency
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
    zlib-dev


# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1

# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1


WORKDIR /usr/src/app
COPY ./requirements.txt .
COPY ./my_project_name .


RUN pip install --upgrade pip
RUN pip install -r requirements.txt


RUN adduser -D myuser
USER myuser


EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "my_project_name.wsgi"]
