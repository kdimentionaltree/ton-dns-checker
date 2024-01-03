# First Stage: Build TONLib (builder)
FROM ubuntu:20.04 as builder

# Install basic tools and dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata && \
    apt-get install -y build-essential cmake clang openssl libssl-dev zlib1g-dev gperf wget git curl libreadline-dev ccache libmicrohttpd-dev ninja-build pkg-config libsecp256k1-dev libsodium-dev

# Clone the TON repository and check out a specific branch
ARG TON_REPO=ton-blockchain
ARG TON_REPO_BRANCH=master
WORKDIR /ton
RUN git clone --recurse-submodules https://github.com/${TON_REPO}/ton.git . && \
    git checkout ${TON_REPO_BRANCH}

# Build TONLib
RUN mkdir build && \
    cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release -GNinja .. && \
    ninja -j 0 dht-resolve dht-ping-servers

# Second Stage: Frontend Build (frontend_builder)
FROM node:18-bullseye as frontend_builder
ARG REACT_APP_API_URL
ARG REACT_APP_API_KEY

# Copy frontend code and build
WORKDIR /app
COPY frontend/ ./
RUN yarn install && \
    yarn build

# Third Stage: Final Runtime Environment Setup
FROM ubuntu:20.04

# Install runtime dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata && \
    apt-get install -y openssl libssl-dev wget curl libatomic1 zlib1g-dev gperf wget git curl libreadline-dev ccache libmicrohttpd-dev dnsutils python3-dev python3-pip && \
    pip3 install --no-cache-dir -U pip wheel

# Copy the built TONLib binary files
COPY --from=builder /ton/build/dht/dht-resolve /app/binaries/dht-resolve
COPY --from=builder /ton/build/dht/dht-ping-servers /app/binaries/dht-ping-servers
RUN chmod +x /app/binaries/dht-resolve /app/binaries/dht-ping-servers

# Copy and deploy the frontend
COPY --from=frontend_builder /app/build /app/static

# Install Python dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy DNS Checker backend code
COPY dnschecker/ ./dnschecker/

# Set default command for container startup
ENTRYPOINT [ "/bin/bash" ]
