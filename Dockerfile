# 第一阶段：构建 TONLib (builder)
FROM ubuntu:20.04 as builder

# 安装基本工具和依赖
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata && \
    apt-get install -y build-essential cmake clang openssl libssl-dev zlib1g-dev gperf wget git curl libreadline-dev ccache libmicrohttpd-dev

# 克隆 TON 仓库并检出指定分支
ARG TON_REPO=SpyCheese
ARG TON_REPO_BRANCH=dht-ping
WORKDIR /ton
RUN git clone --recurse-submodules https://github.com/${TON_REPO}/ton.git . && \
    git checkout ${TON_REPO_BRANCH}

# 构建 TONLib
RUN mkdir build && \
    cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release .. && \
    cmake --build . -j$(nproc) --target dht-resolve dht-ping-servers

# 第二阶段：构建前端 (frontend_builder)
FROM node:18-bullseye as frontend_builder
ARG REACT_APP_API_URL
ARG REACT_APP_API_KEY

# 复制前端代码并构建
WORKDIR /app
COPY frontend/ ./
RUN yarn install && \
    yarn build

# 第三阶段：最终运行环境配置
FROM ubuntu:20.04

# 安装运行时依赖
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata && \
    apt-get install -y openssl libssl-dev wget curl libatomic1 zlib1g-dev gperf wget git curl libreadline-dev ccache libmicrohttpd-dev dnsutils python3-dev python3-pip && \
    pip3 install --no-cache-dir -U pip wheel

# 复制构建好的 TONLib 二进制文件
COPY --from=builder /ton/build/dht/dht-resolve /app/binaries/dht-resolve
COPY --from=builder /ton/build/dht/dht-ping-servers /app/binaries/dht-ping-servers
RUN chmod +x /app/binaries/dht-resolve /app/binaries/dht-ping-servers

# 复制并部署前端
COPY --from=frontend_builder /app/build /app/static

# 安装 Python 依赖
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 复制 DNS 检查器后端代码
COPY dnschecker/ ./dnschecker/

# 设置容器启动时的默认命令
ENTRYPOINT [ "/bin/bash" ]
