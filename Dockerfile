FROM python:3.10

RUN echo "vm.overcommit_memory = 1" >> /etc/sysctl.conf
RUN apt-get update && apt-get install -y sysfsutils

WORKDIR /app

COPY ./env/base.txt /app/env/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    VIRTUAL_ENV=/venv \
    PATH=/venv/bin:$PATH

RUN python -m venv $VIRTUAL_ENV && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/env/base.txt

COPY . /app

COPY ./entrypoint.sh /app
RUN chmod +x /app/entrypoint.sh

RUN chgrp -R 0 /app && \
    chmod -R g+rwX /app

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
