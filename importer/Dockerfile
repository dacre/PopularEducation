FROM alpine:latest

ENV APP_USER appuser

RUN adduser -g "App User" -D $APP_USER

RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    pip3 install bs4 && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi

ADD . /importer
WORKDIR /importer

COPY /db/db.csv /importer/db/

COPY crontab /var/spool/cron/crontabs/$APP_USER
RUN chmod 0600 /var/spool/cron/crontabs/$APP_USER
RUN chmod 777 /importer/*
RUN chmod 777 /importer/db/*

CMD ["crond", "-f", "-d", "8"]

