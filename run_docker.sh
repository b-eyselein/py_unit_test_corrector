#!/usr/bin/env bash

EX=${1:?"Error: exercise name / folder is not defined!"}

if [[ ${EX} == */ ]]; then
    EX=${EX::-1}
fi

IMG_NAME=ls6uniwue/py_unit_test_corrector:0.3.0

RES_FILE=results/${EX}_result.json
CONF_FILE_NAME=test_data.json

CONF_FILE=${EX}/${CONF_FILE_NAME}

# Build image
docker build -t ${IMG_NAME} .

#docker image prune -f

if [[ ! -f ${CONF_FILE} ]]; then
    printf '\033[0;31mThere is no local config file for exercise!\n'
    exit 10
fi

if [[ ! -f ${RES_FILE} ]]; then
    mkdir -p results/
    touch ${RES_FILE}
else
    truncate -s 0 ${RES_FILE}
fi

docker run -it  \
    -v $(pwd)/${CONF_FILE}:/data/${CONF_FILE_NAME}:ro \
    -v $(pwd)/${EX}/:/data/${EX}/ \
    -v $(pwd)/${RES_FILE}:/data/result.json \
    ${IMG_NAME}