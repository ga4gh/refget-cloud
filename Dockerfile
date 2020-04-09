FROM python:3.7.7-buster

USER root

WORKDIR /usr/src/app

COPY config config
COPY scripts scripts
COPY setup.py setup.py
COPY ga4gh ga4gh
COPY README.md README.md

RUN python setup.py install
RUN chmod 755 ./scripts/docker/run.sh

CMD ./scripts/docker/run.sh
