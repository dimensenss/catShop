FROM python:3.9-alpine3.16

COPY requirements.txt /temp/requirements.txt
RUN apk add postgresql-client build-base postgresql-dev
RUN pip install -r /temp/requirements.txt

COPY . /app
WORKDIR /app
EXPOSE 8000

RUN adduser --disabled-password simple_shop-user
USER simple_shop-user