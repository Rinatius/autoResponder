FROM python:3.9-slim

ENV PYTHONBUFFERED 1
RUN set -xe \
    && apt update \
    && apt upgrade -y

RUN pip install -U pipenv
RUN pip install --no-cache-dir openai
RUN pip install --no-cache-dir google-cloud-translate

WORKDIR /app
COPY ./Pipfile /app/Pipfile
COPY ./Pipfile.lock /app/Pipfile.lock
RUN pipenv install --system --deploy --ignore-pipfile
RUN python -m nltk.downloader punkt

COPY . /app

# Comment out the EXPOSE and CMD lines for now

# EXPOSE 8000
# CMD python manage.py runserver 0.0.0.0:8000
