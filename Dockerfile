FROM python:3.13-alpine3.22
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories && \
    echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
ENV TZ=Europe/Moscow
RUN apk update \
    && apk upgrade musl \
    && apk add --no-cache tzdata \
    && cp /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo "$TZ" > /etc/timezone
COPY ./requirements.txt fastapi_app_template/requirements.txt
RUN apk add --no-cache --virtual .build-deps \
    build-base gcc musl-dev python3-dev librdkafka-dev \
    openssl-dev cyrus-sasl-dev zlib-dev lz4-dev zstd-dev \
    && apk add --no-cache librdkafka \
    && pip install --no-cache-dir -r fastapi_app_template/requirements.txt \
    && apk del .build-deps
COPY . /fastapi_app_template
WORKDIR /fastapi_app_template
ENTRYPOINT ["python3", "main.py"]