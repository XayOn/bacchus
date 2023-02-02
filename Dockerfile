FROM python:3.11-slim

WORKDIR /app

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    VIRTUAL_ENV=/opt/venv \
    step=first

RUN apt-get update &&\
    pip install hatch &&\
    hatch build &&\
    pip install build/*

COPY install.sh /

ENTRYPOINT /install.sh
