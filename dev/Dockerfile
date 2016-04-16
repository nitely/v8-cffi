FROM ubuntu:14.04
MAINTAINER Esteban Castro Borsani <ecastroborsani@gmail.com>

# todo: change to ubuntu 15

RUN apt-get update \
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
RUN git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git \
    && cd /code/build/depot_tools \
    && git checkout ef7c68c57f20196b27b2059cd28f5f28bb22435a
ENV PATH /code/build/depot_tools:$PATH

# Setup V8 (with depot-tools)
RUN fetch v8 \
    && cd /code/build/v8 \
    && git checkout c4b0b1439529247be31cff87f3028a7b41d22915 \
    && gclient sync

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
