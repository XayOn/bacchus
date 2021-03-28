FROM python:3.9.1-slim as build

WORKDIR /app

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_PATH=/opt/poetry \
    VENV_PATH=/opt/venv \
    POETRY_VERSION=1.1.4

RUN apt-get update \
    && apt-get install --no-install-recommends -y git curl graphviz build-essential\
    && curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python \
    && mv /root/.poetry $POETRY_PATH \
    && ls $POETRY_PATH \
    && $POETRY_PATH/bin/poetry --version && python -m venv $VENV_PATH \
    && $POETRY_PATH/bin/poetry config virtualenvs.create false \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
RUN $POETRY_PATH/bin/poetry install --no-dev --no-root
COPY . ./ 
RUN $POETRY_PATH/bin/poetry install --no-dev

FROM python:3.9.1-slim
ENV PATH="$VENV_PATH/bin:$PATH" \
    VENV_PATH=/opt/venv

RUN ln -sf /usr/share/zoneinfo/UTC /etc/localtime

COPY --from=build $VENV_PATH $VENV_PATH
COPY --from=build /app/ /app/

ENTRYPOINT bacchus 
