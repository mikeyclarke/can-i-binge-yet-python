FROM python:3.10.5-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ=UTC

RUN apk update && apk --no-cache add \
    libffi-dev gcc musl-dev python3-dev openssl-dev cargo

RUN pip install -U pip setuptools wheel
RUN pip install pdm

WORKDIR /var/bingeable

COPY . .

RUN pdm install

CMD ["pdm", "run", "start"]
