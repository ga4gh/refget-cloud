#!/bin/bash

PROPERTIES_FILE="./config/application.properties"
CMD="refget-server"

python scripts/docker/configure.py

if [[ -f ${PROPERTIES_FILE} ]]; then CMD="${CMD} --properties-file ${PROPERTIES_FILE}"; fi

$CMD
