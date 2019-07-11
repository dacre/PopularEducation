FROM alpine:latest

ENV APP_USER appuser

RUN adduser -g "App User" -D $APP_USER

RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    pip3 install bs4 && \
    pip3 install requests && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi

ADD . /importer
WORKDIR /importer
COPY crontab /var/spool/cron/crontabs/$APP_USER
RUN chmod 705 /var/spool/cron/crontabs/$APP_USER
RUN chmod 705 /importer/*
RUN chmod 707 /importer/db/
#TODO use this, but fix crond för USER $APP_USER

CMD ["crond", "-f", "-d", "8"]

