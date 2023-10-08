FROM python:3.10-buster

RUN echo "vm.overcommit_memory = 1" >> /etc/sysctl.conf

WORKDIR /djnapp

COPY ./env/base.txt /djnapp/env/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    VIRTUAL_ENV=/venv \
    PATH=/venv/bin:$PATH

RUN python -m venv $VIRTUAL_ENV && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r /djnapp/env/base.txt

COPY . /djnapp

COPY ./entrypoint.sh /djnapp
RUN chmod a+x /djnapp/entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/djnapp/entrypoint.sh"]
