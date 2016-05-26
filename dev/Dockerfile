FROM centos:6.7
MAINTAINER Esteban Castro Borsani <ecastroborsani@gmail.com>

# Be aware this is a throw-away image,
# its size is quite big (many layers)
# coz that way we can retry a failed step.

# Requirements:
# glibc 2.8 (CentOS 6 has 2.12)
# Python +2.7.9 (with SSL support)
# Git +2.7
# Tar +1.28 (with bzip2 support)
# GCC +4.8
# G++ +4.8

#
# The "touch /var/lib/rpm/* \"
# before every "yum install"
# is a workaround to
# "Rpmdb checksum is invalid: dCDPT(pkg checksums)"
# errors, for builds in hub.docker.com
# See: https://github.com/docker/docker/issues/10180
#


RUN mkdir -p /code/build
WORKDIR /code/build

RUN touch /var/lib/rpm/* \
    && yum install -y \
    openssl \
    openssl-devel \
    libffi-devel \
    wget \
    make \
    gcc \
    tar \
    && yum clean all

# GCC 4.8.2
RUN wget http://people.centos.org/tru/devtools-2/devtools-2.repo -O /etc/yum.repos.d/devtools-2.repo \
    && touch /var/lib/rpm/* \
    && yum install -y \
    devtoolset-2-gcc \
    devtoolset-2-binutils \
    devtoolset-2-gcc-c++ \
    && rm /etc/yum.repos.d/devtools-2.repo \
    && yum clean all

# Python 2.7
RUN wget http://www.python.org/ftp/python/2.7.11/Python-2.7.11.tgz \
    && tar -xzvf Python-2.7.11.tgz \
    && cd Python-2.7.11 \
    && ./configure \
    && make altinstall

RUN python2.7 -m ensurepip \
    && python2.7 -m pip install pyOpenSSL==16.0.0

# Git 2
RUN touch /var/lib/rpm/* \
    && yum install -y \
    curl-devel \
    expat-devel \
    gettext-devel \
    openssl-devel \
    perl-devel \
    zlib-devel \
    && yum clean all

RUN wget https://www.kernel.org/pub/software/scm/git/git-2.7.4.tar.gz \
    && tar xzf git-2.7.4.tar.gz \
    && cd git-2.7.4 \
    && make prefix=/usr/local/git all \
    && make prefix=/usr/local/git install
ENV PATH /usr/local/git/bin:$PATH

# Tar 1.28
RUN touch /var/lib/rpm/* \
    && yum install -y \
    bzip2 \
    bzip2-devel \
    && yum clean all

ENV FORCE_UNSAFE_CONFIGURE=1
RUN wget http://ftp.gnu.org/gnu/tar/tar-1.29.tar.gz \
    && tar xzf tar-1.29.tar.gz \
    && cd tar-1.29 \
    && ./configure prefix=/usr/local/tar \
    && make \
    && make install

# Set Python 2.7 as default
# Set tar 1.28 as default
RUN cd /usr/local/bin \
    && ln -s python2.7 python \
    && ln -s /usr/local/tar/bin/tar tar

# Setup depot-tools
# Remove .git to disable auto update
RUN git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git \
    && cd depot_tools \
    && git checkout ef7c68c57f20196b27b2059cd28f5f28bb22435a \
    && rm -rf .git
ENV PATH /code/build/depot_tools:$PATH

# Disable auto update - alternative
ENV DEPOT_TOOLS_UPDATE 0

# Setup V8 (with depot-tools)
# and show V8 version
RUN fetch v8 \
    && cd v8 \
    && git checkout 1c998eae01e53610a852e6b2d9b7d2822eefe8f3 \
    && gclient sync \
    && head -1 ChangeLog

ENV CFLAGS -fPIC
ENV CXXFLAGS -fPIC
RUN cd v8 \
    && source /opt/rh/devtoolset-2/enable \
    && make x64.release -j4 GYPFLAGS="-Dclang=0"

# Restore default Python
# Restore default tar
RUN cd /usr/local/bin \
    && rm python \
    && rm tar

RUN mkdir -p /code/v8/release

# Convert thin archives into normal ones,
# the alternative is to add 'standalone_static_library': 1
# to GYP build file
RUN cd /code/build/v8/out/x64.release \
    && for lib in `find -name '*.a'`; \
        do ar -t $lib | xargs ar Drvs $lib.new \
           && mv -v $lib.new /code/v8/release/$(basename $lib); \
    done

# Copy required bin files
# and API headers
RUN cd v8 \
    && cp -v LICENSE.v8 /code/v8/LICENSE.v8 \
    && cp -v -R include/ /code/v8/include/ \
    \
    && cd /code/build/v8/out/x64.release \
    && cp -v natives_blob.bin /code/v8/natives_blob.bin \
    && cp -v snapshot_blob.bin /code/v8/snapshot_blob.bin

WORKDIR /code
