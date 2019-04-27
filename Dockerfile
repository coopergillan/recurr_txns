FROM python:3.7.3-stretch

RUN \
    pip install \
    numpy==1.16.3 \
    pandas==0.24.2 \
    PyYAML==5.1

WORKDIR /app
COPY . /app

ENTRYPOINT ["python", "recurr_txns.py"]
