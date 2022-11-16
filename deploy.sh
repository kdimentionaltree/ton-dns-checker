#!/bin/bash
set -e
docker compose build
docker compose push

export $(cat .env) > /dev/null || echo "No .env file"
export TONCENTER_ENV=${1:-stage}

# toncenter-deploy
docker stack deploy -c docker-compose.yaml ${TONCENTER_ENV}

