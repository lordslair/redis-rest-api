FROM alpine:3.18

RUN adduser -h /code -u 1000 -D -H api

ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

COPY --chown=api:api requirements.txt /requirements.txt
COPY --chown=api:api /code            /code

WORKDIR /code
ENV PATH="/code/.local/bin:${PATH}"

RUN apk update --no-cache \
    && apk add --no-cache \
        "python3>=3.11" \
        "tzdata>=2023" \
    && apk add --no-cache --virtual .build-deps \
        "gcc=~12.2" \
        "g++=~12.2" \
        "libc-dev=~0.7" \
        "libffi-dev=~3.4" \
        "python3-dev>=3.11" \
    && su api -c \
        "python3 -m ensurepip --upgrade \
        && pip3 install --user -U -r /requirements.txt" \
    && rm /requirements.txt \
    && apk del .build-deps

USER api

ENTRYPOINT ["/code/app.py"]
