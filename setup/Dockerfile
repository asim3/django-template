FROM python:3.11-slim-bullseye AS base

FROM base AS builder

RUN apt-get -y update && apt-get -y install gcc python3-dev libpq-dev

COPY ./requirements.txt /requirements.txt

RUN pip wheel --wheel-dir=/root/wheels -r /requirements.txt

LABEL org.opencontainers.image.source=https://github.com/asim3/my_project_name
LABEL org.opencontainers.image.description="Django: my_project_name"



FROM base

RUN apt-get -y update && apt-get -y install libpq5

RUN adduser --system --shell /bin/bash --uid 1000 --group --disabled-password --disabled-login d_user

ENV APP_HOME=/home/d_user/web

RUN install -d -m 0750 -o d_user -g d_user $APP_HOME

COPY --from=builder /root/wheels /root/wheels

COPY --from=builder /requirements.txt $APP_HOME/requirements.txt

RUN pip install --no-index --find-links=/root/wheels -r $APP_HOME/requirements.txt

COPY --chown=d_user:d_user --chmod=550 ./my_project_name $APP_HOME

WORKDIR $APP_HOME

USER d_user

ENTRYPOINT ["/bin/sh", "-c"]

CMD ["python3 manage.py runserver 0.0.0.0:8000"]
