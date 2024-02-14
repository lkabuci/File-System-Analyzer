FROM python:3.9-slim-bookworm

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY requirements.txt /tmp/requirements.txt

WORKDIR /app

RUN apt-get update &&\
    apt-get install -y --no-install-recommends libmagic1 &&\
    python3 -m venv $VIRTUAL_ENV &&\
    pip install --upgrade pip &&\
    pip install --no-cache -r /tmp/requirements.txt &&\
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT [ "python3" ]
