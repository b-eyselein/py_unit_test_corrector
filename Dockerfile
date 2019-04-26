FROM python:3-alpine

WORKDIR /data

COPY main.py main_helpers.py /data/

ENTRYPOINT python3 main.py