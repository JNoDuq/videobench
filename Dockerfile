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
	python3-venv \
        yasm \
        pkg-config \
	libdav1d-dev \
        && \
        apt-get clean && \
        rm -rf /var/lib/apt/lists


# install python requirements
        #RUN pip3 install --upgrade pip  --break-system-packages
        RUN pip3 install --no-cache-dir meson cython numpy  --break-system-packages

# setup environment
        ENV PATH=/vmaf:/vmaf/libvmaf/build/tools:$PATH


RUN \
        mkdir /tmp/vmaf \
        && cd /tmp/vmaf \
        && git clone https://github.com/Netflix/vmaf.git . \
	&& sed -i 's/python3\.10/python3/g' Makefile \
        && make PYTHON=python3 PYTHON_ECEX=python3\
        && make install \
        && cp -r ./model /usr/local/share/ \
        && rm -r /tmp/vmaf


RUN \
        mkdir /tmp/ffmpeg \
        && cd /tmp/ffmpeg \
        && git clone https://git.ffmpeg.org/ffmpeg.git . \
        && ./configure --enable-libdav1d --enable-libvmaf --enable-version3 --pkg-config-flags="--static" \
        && make -j 8 install \
        && rm -r /tmp/ffmpeg



RUN \
        mkdir -p /home/shared-vmaf

RUN \
        ldconfig
