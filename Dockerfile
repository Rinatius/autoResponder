FROM python:3.7-slim

ENV PYTHONBUFFERED 1
RUN set -xe \
    && apt update \
    && apt upgrade -y

RUN pip install -U pipenv

WORKDIR /app
COPY ./Pipfile /app/Pipfile
COPY ./Pipfile.lock /app/Pipfile.lock
RUN pipenv install --system --deploy --ignore-pipfile
COPY . /app

EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000
