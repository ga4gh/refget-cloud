FROM python:3.7.7-buster

USER root

WORKDIR /usr/src/app

COPY config config
COPY scripts scripts
COPY setup.py setup.py
COPY lib lib
COPY README.md README.md
COPY web web

##################################################
# GET SWAGGER UI, MOVE TO PUBLIC HTML FOLDER
##################################################

RUN wget https://github.com/swagger-api/swagger-ui/archive/v3.25.0.tar.gz \
    && tar -zxvf v3.25.0.tar.gz

RUN mv web/swagger-ui/index.html . \
    && cp swagger-ui-3.25.0/dist/* web/swagger-ui/ \
    && mv ./index.html web/swagger-ui/

RUN python setup.py install

RUN chmod 755 ./scripts/docker/run.sh

CMD ./scripts/docker/run.sh
