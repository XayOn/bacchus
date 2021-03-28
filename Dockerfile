FROM python:3.9.1-slim as build

WORKDIR /app

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_PATH=/opt/poetry \
    VIRTUAL_ENV=/opt/venv \
    POETRY_VERSION=1.1.4 \
    PATH=$PATH:/root/.poetry/bin/

RUN apt-get update \
    && apt-get install --no-install-recommends -y git curl graphviz build-essential\
    && python -m venv $VIRTUAL_ENV \
    && curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python \ 
    && poetry config virtualenvs.create false \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
RUN poetry install --no-dev --no-root
COPY . ./ 
RUN poetry install --no-dev
# RUN pip install .

FROM python:3.9.1-slim
ENV PATH="$VIRTUAL_ENV/bin:$PATH" \
    VIRTUAL_ENV=/opt/venv

RUN ln -sf /usr/share/zoneinfo/UTC /etc/localtime

COPY --from=build $VIRTUAL_ENV $VIRTUAL_ENV
COPY --from=build /app/ /app/

ENTRYPOINT /opt/venv/bacchus 
