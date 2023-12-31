#!/bin/bash
set -e

# 设置默认环境或使用脚本的第一个参数
export TONCENTER_ENV=${1:-stage}
STACK_NAME="${TONCENTER_ENV}-dns-checker"
echo "Stack: ${STACK_NAME}"

# 检查是否有针对特定环境的 .env 文件
if [ -f ".env.${TONCENTER_ENV}" ]; then
    echo "Found env for ${TONCENTER_ENV}"
    ENV_FILE=".env.${TONCENTER_ENV}"
elif [ -f ".env" ]; then
    echo "Found default .env"
    ENV_FILE=".env"
fi

# 加载环境变量
if [ ! -z "${ENV_FILE}" ]; then
    set -a  # 自动导出所有变量
    source ${ENV_FILE}
    set +a
fi

# 根据环境选择配置文件
if [[ "${TONCENTER_ENV}" == "testnet" ]]; then
    echo "Using testnet config"
    export TON_LITESERVER_CONFIG=private/testnet.json
else
    echo "Using mainnet config"
    export TON_LITESERVER_CONFIG=private/mainnet.json
fi

# 构建并推送 Docker 镜像
docker compose build
docker compose push

# 使用 docker-compose.yaml 部署堆栈
docker stack deploy -c docker-compose.yaml ${STACK_NAME}

# 将服务连接到全局网络（如果存在）
GLOBAL_NET_NAME=$(docker network ls --format '{{.Name}}' --filter NAME=toncenter-global)
if [ ! -z "$GLOBAL_NET_NAME" ]; then
    echo "Found network: ${GLOBAL_NET_NAME}"
    docker service update --detach --network-add name=${GLOBAL_NET_NAME},alias=${TONCENTER_ENV}-dns-checker ${STACK_NAME}_dns-checker
fi
