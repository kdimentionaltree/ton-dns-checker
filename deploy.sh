#!/bin/bash
set -e

# Set the default environment or use the first argument of the script
export TONCENTER_ENV=${1:-stage}
STACK_NAME="${TONCENTER_ENV}-dns-checker"
echo "Stack: ${STACK_NAME}"

# Check for the existence of an environment-specific .env file
if [ -f ".env.${TONCENTER_ENV}" ]; then
    echo "Found env for ${TONCENTER_ENV}"
    ENV_FILE=".env.${TONCENTER_ENV}"
elif [ -f ".env" ]; then
    echo "Found default .env"
    ENV_FILE=".env"
fi

# Load environment variables
if [ ! -z "${ENV_FILE}" ]; then
    set -a  # Automatically export all variables
    source ${ENV_FILE}
    set +a
fi

# Choose configuration file based on environment
if [[ "${TONCENTER_ENV}" == "testnet" ]]; then
    echo "Using testnet config"
    export TON_LITESERVER_CONFIG=private/testnet.json
else
    echo "Using mainnet config"
    export TON_LITESERVER_CONFIG=private/mainnet.json
fi

# Build and push Docker images
docker compose build
docker compose push

# Deploy the stack using docker-compose.yaml
docker stack deploy -c docker-compose.yaml ${STACK_NAME}

# Connect the service to the global network if it exists
GLOBAL_NET_NAME=$(docker network ls --format '{{.Name}}' --filter NAME=toncenter-global)
if [ ! -z "$GLOBAL_NET_NAME" ]; then
    echo "Found network: ${GLOBAL_NET_NAME}"
    docker service update --detach --network-add name=${GLOBAL_NET_NAME},alias=${TONCENTER_ENV}-dns-checker ${STACK_NAME}_dns-checker
fi
