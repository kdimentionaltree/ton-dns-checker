#!/bin/bash

# 退出脚本，如果任何命令执行失败
set -e

# 创建一个目录来存储配置文件，如果目录不存在
mkdir -p private

# 下载 TON 主网配置文件
# -q: 安静模式，不输出任何信息
# -O: 指定输出文件名
echo "Downloading TON mainnet configuration..."
wget https://ton.org/global-config.json -q -O private/mainnet.json

# 下载 TON 测试网配置文件
echo "Downloading TON testnet configuration..."
wget https://ton-blockchain.github.io/testnet-global.config.json -q -O private/testnet.json
