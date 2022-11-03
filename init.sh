#!/bin/bash
set -e

mkdir -p private
wget https://ton.org/global-config.json -q -O private/global-config.json
# wget https://ton-blockchain.github.io/testnet-global.config.json -q-O private/global-config.json # testnet config
