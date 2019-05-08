FROM python:3-alpine

RUN apk update && apk upgrade && pip install -U pip jsonschema

WORKDIR /data

COPY main.py main_helpers.py test_data.schema.json /data/

ENTRYPOINT python3 main.py