FROM python:3.10.0-alpine


ENV PYTHONDONTWRITEBYTECODE=1


ENV PYTHONUNBUFFERED=1


WORKDIR /code/backend


RUN pip install --upgrade pip


COPY requirements.txt /code/backend/


RUN pip install -r /code/backend/requirements.txt


# RUN apt-get update && apt-get install -y gcc python3-dev default-libmysqlclient-dev pkg-config
# RUN default-libmysqlclient-dev pkg-config
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    mariadb-connector-c-dev \
    pkgconfig


# RUN pip install mysqlclient

RUN pip install drf_spectacular


COPY . /code/backend/