FROM python:3.9-alpine3.16
LABEL maintaner="denniso2"

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements-dev.txt /tmp/requirements-dev.txt
COPY ./ /app
WORKDIR /app
EXPOSE 8000

RUN pip install --upgrade pip && \
    apk add curl && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    curl -sfL https://github.com/powerman/dockerize/releases/download/v0.16.3/dockerize-`uname -s`-`uname -m`\
     | install /dev/stdin /usr/local/bin/dockerize && \
    pip install -r /tmp/requirements.txt && \
    pip install -r /tmp/requirements-dev.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

USER django-user