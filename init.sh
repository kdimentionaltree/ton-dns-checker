#!/bin/bash

# Exit the script if any command fails
set -e

# Create a directory to store configuration files if it doesn't exist
mkdir -p private

# Download TON mainnet configuration file
# -q: Quiet mode, no output information
# -O: Specify the output file name
echo "Downloading TON mainnet configuration..."
wget https://ton.org/global-config.json -q -O private/mainnet.json

# Download TON testnet configuration file
echo "Downloading TON testnet configuration..."
wget https://ton-blockchain.github.io/testnet-global.config.json -q -O private/testnet.json
