FROM ubuntu:12.04
MAINTAINER Esteban Castro Borsani <ecastroborsani@gmail.com>

# We build with an old Ubuntu version
# for wider compatibility (glibc 2.15)

# Install required GCC>=4.8
# and git 2.x
RUN apt-get update \
    && apt-get install -y \
    python-software-properties \
    && add-apt-repository -y ppa:ubuntu-toolchain-r/test \
    && apt-get update \
    && apt-get install -y \
    gcc-4.9 \
    g++-4.9 \
    && update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.9 50 \
    && update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.9 50 \
    && add-apt-repository ppa:git-core/ppa \
    && apt-get update \
    && apt-get install -y \
    git \
    python \
    python-dev \
    python-distribute \
    python-pip \
    build-essential \
    libffi-dev \
    g++-multilib

RUN mkdir -p /code/build
WORKDIR /code/build

# Setup depot-tools
# Remove .git to disable auto update
RUN git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git \
    && cd /code/build/depot_tools \
    && git checkout ef7c68c57f20196b27b2059cd28f5f28bb22435a \
    && rm -rf .git
ENV PATH /code/build/depot_tools:$PATH

# Disable auto update - alternative
ENV DEPOT_TOOLS_UPDATE=0

# Setup V8 (with depot-tools)
# and show V8 version
RUN fetch v8 \
    && cd /code/build/v8 \
    && git checkout 1c998eae01e53610a852e6b2d9b7d2822eefe8f3 \
    && gclient sync \
    && head -1 ChangeLog

WORKDIR /code/build/v8

ENV CFLAGS -fPIC
ENV CXXFLAGS -fPIC
RUN make x64.release -j4

# Convert thin archives into normal ones,
# the alternative is to add 'standalone_static_library': 1
# to GYP build file
RUN cd /code/build/v8/out/x64.release \
    && for lib in `find -name '*.a'`; \
        do ar -t $lib | xargs ar rvs $lib.new && mv -v $lib.new $lib; \
    done

WORKDIR /code
