FROM python:3.12-slim-bookworm

COPY requirements.txt /tmp/requirements.txt

WORKDIR /app

RUN set -ex &&\
    pip install --upgrade pip &&\
    pip install --no-cache -r /tmp/requirements.txt &&\
    rm -rf /var/lib/apt/lists/*

COPY . /app

ENTRYPOINT [ "pytest", "-v", "tests/" ]
