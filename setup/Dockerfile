FROM python:3.10-slim-bullseye AS builder

RUN apt-get -y update && apt-get -y install gcc python3-dev libpq-dev

COPY ./requirements.txt /requirements.txt

RUN pip wheel --wheel-dir=/root/wheels -r /requirements.txt


# https://morioh.com/a/d777482dea93/how-to-building-minimal-docker-containers-for-python-applications
FROM python:3.10-slim-bullseye

RUN adduser --system --shell /bin/bash --uid 1000 --group --disabled-password --disabled-login d_user

ENV APP_HOME=/home/d_user/web

RUN install -d -m 0750 -o d_user -g d_user $APP_HOME $APP_HOME/tmp

COPY --from=builder /root/wheels /root/wheels

COPY --from=builder /requirements.txt $APP_HOME/requirements.txt

RUN pip install --no-index --find-links=/root/wheels -r $APP_HOME/requirements.txt

COPY --chown=d_user:d_user --chmod=550 ./my_project_name $APP_HOME

WORKDIR $APP_HOME

USER d_user

ENTRYPOINT ["/bin/sh", "-c"]

CMD ["gunicorn --bind :8000 --workers 3 my_project_name.wsgi"]
