FROM ubuntu:20.04 as builder

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata

RUN apt install -y build-essential cmake clang openssl libssl-dev zlib1g-dev gperf wget git curl libreadline-dev ccache libmicrohttpd-dev

# build tonlib
WORKDIR /

# remove /tree/<commit> to build master branch
ARG TON_REPO=SpyCheese
ARG TON_REPO_BRANCH=dht-ping
RUN echo "Branch: ${TON_REPO_BRANCH}" && \
    git clone --recurse-submodules https://github.com/${TON_REPO}/ton.git && \
    cd /ton && git checkout ${TON_REPO_BRANCH}    

# fix lib version and patch logging
WORKDIR /ton
RUN mkdir /ton/build
WORKDIR /ton/build
ENV CC clang
ENV CXX clang++
RUN cmake -DCMAKE_BUILD_TYPE=Release ..
RUN cmake --build . -j$(nproc) --target dht-resolve dht-ping-servers


FROM node:18-bullseye as frontend_builder
ARG REACT_APP_API_URL
ARG REACT_APP_API_KEY

WORKDIR /app
COPY frontend/ /app
RUN echo "env: ${REACT_APP_API_URL} ${REACT_APP_API_KEY}" && yarn install
RUN yarn build


FROM ubuntu:20.04

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata

RUN apt install -y openssl libssl-dev wget curl libatomic1 zlib1g-dev gperf wget git curl libreadline-dev ccache libmicrohttpd-dev dnsutils
RUN apt install -y python3-dev python3-pip
RUN pip3 install --no-cache-dir -U pip wheel

# copy binaries
COPY --from=builder /ton/build/dht/dht-resolve /app/binaries/dht-resolve
COPY --from=builder /ton/build/dht/dht-ping-servers /app/binaries/dht-ping-servers
RUN chmod +x /app/binaries/dht-resolve /app/binaries/dht-ping-servers

# copy frontend
COPY --from=frontend_builder /app/build /app/static

WORKDIR /app
ADD requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt
COPY dnschecker/ /app/dnschecker/

ENTRYPOINT [ "/bin/bash" ]
