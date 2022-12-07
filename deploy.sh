#!/bin/bash
set -e

export TONCENTER_ENV=${1:-stage}
STACK_NAME="${TONCENTER_ENV}-dns-checker"
echo "Stack: ${STACK_NAME}"

if [ -f ".env.${TONCENTER_ENV}" ]; then
    echo "Found env for ${TONCENTER_ENV}"
    ENV_FILE=".env.${TONCENTER_ENV}"
elif [ -f ".env" ]; then
    echo "Found default .env"
    ENV_FILE=".env"
fi

# load environment variables
if [ ! -z "${ENV_FILE}" ]; then
    # export $(cat ${ENV_FILE}) > /dev/null|| echo "No .env file"
    set -a
    source ${ENV_FILE}
    set +a
fi

if [[ "${TONCENTER_ENV}" == "testnet" ]]; then
    echo "Using testnet config"
    export TON_LITESERVER_CONFIG=private/testnet.json
else
    echo "Using mainnet config"
    export TON_LITESERVER_CONFIG=private/mainnet.json
fi

# build
docker compose build
docker compose push

# deploy
docker stack deploy -c docker-compose.yaml ${STACK_NAME}

# attach to global network
GLOBAL_NET_NAME=$(docker network ls --format '{{.Name}}' --filter NAME=toncenter-global)

if [ ! -z "$GLOBAL_NET_NAME" ]; then
    echo "Found network: ${GLOBAL_NET_NAME}"
    docker service update --detach --network-add name=${GLOBAL_NET_NAME},alias=${TONCENTER_ENV}-dns-checker ${STACK_NAME}_dns-checker
fi
