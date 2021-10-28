FROM alpine:latest

RUN apk add --no-cache --update python3 py3-pip bash

COPY ./webapp/requirements.txt /tmp/requirements.txt

RUN pip3 install --no-cache-dir -q -r /tmp/requirements.txt

COPY ./webapp /opt/webapp/

WORKDIR /opt/webapp

RUN adduser -D myuser

USER myuser

CMD gunicorn --workers 3 --bind 0.0.0.0:5000 wsgi 
