#!/bin/bash
set -e

export $(cat .env) > /dev/null || echo "No .env file"
export TONCENTER_ENV=${1:-stage}

docker compose build
docker compose push

# toncenter-deploy
docker stack deploy -c docker-compose.yaml ${TONCENTER_ENV}

