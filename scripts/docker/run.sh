#!/bin/bash

PROPERTIES_FILE="./config/application.properties"

python scripts/docker/configure.py
refget-server --properties-file ${PROPERTIES_FILE}
