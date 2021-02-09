FROM python:3.9.1-slim

RUN \
      pip3 install --upgrade pip \
      && pip3 install --no-cache-dir pipenv

WORKDIR /app

COPY ./Pipfile ./Pipfile
COPY ./Pipfile.lock ./Pipfile.lock

RUN pipenv install --deploy

COPY ./lib ./lib
ADD ./input ./input
RUN mkdir results

ENTRYPOINT ["pipenv", "run", "python", "lib/recurr_txns.py"]
