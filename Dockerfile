FROM python:3.9-slim-bookworm

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY requirements.txt /tmp/requirements.txt

WORKDIR /app

RUN set -ex &&\
    python3 -m venv $VIRTUAL_ENV &&\
    pip install --upgrade pip &&\
    pip install --no-cache -r /tmp/requirements.txt &&\
    rm -rf /var/lib/apt/lists/*

COPY . /app

ENTRYPOINT [ "pytest", "-v", "tests/" ]
