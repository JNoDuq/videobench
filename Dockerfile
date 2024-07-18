FROM ubuntu

ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update


# get and install building tools
RUN \
        apt-get update && \
        apt-get install -y --no-install-recommends \
        build-essential \
        git \
        ninja-build \
        nasm \
        doxygen \
        python3 \
        python3-dev \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        python3-tk \
        yasm \
        pkg-config \
        python3-venv \
        && \
        apt-get clean && \
        rm -rf /var/lib/apt/lists




RUN \
        mkdir /tmp/vmaf \
        && cd /tmp/vmaf \
        && git clone https://github.com/Netflix/vmaf.git . \
        && python3 -mvenv .venv \
        && .venv/bin/pip install --upgrade pip \
        && .venv/bin/pip install --no-cache-dir meson cython numpy setuptools \
        && make \
        && make install \
        && cp -r ./model /usr/local/share/ \
        && rm -r /tmp/vmaf


RUN \
        mkdir /tmp/ffmpeg \
        && cd /tmp/ffmpeg \
        && git clone https://git.ffmpeg.org/ffmpeg.git . \
        && ./configure --enable-libvmaf --enable-version3 --pkg-config-flags="--static" \
        && make -j 8 install \
        && rm -r /tmp/ffmpeg



RUN \
        mkdir -p /home/shared-vmaf

RUN \
        ldconfig
