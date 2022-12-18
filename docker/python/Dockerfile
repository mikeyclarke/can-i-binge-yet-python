FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.14 \
    TZ=UTC

RUN apk update && apk --no-cache add \
    libffi-dev gcc musl-dev python3-dev openssl-dev cargo

RUN pip install -U pip setuptools wheel poetry==$POETRY_VERSION

WORKDIR /var/bingeable

COPY . .

RUN poetry install --no-interaction

CMD ["poetry", "run", "gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "wsgi:application"]
