FROM ubuntu

ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update -qq

RUN \
	apt-get install -y build-essential git make \
          ninja-build \
          nasm \
          python3 \
          python3-dev \
          python3-pip \
          python3-setuptools \
          python3-tk \
        && pip3 install --upgrade pip \
        && pip install numpy scipy matplotlib notebook pandas sympy nose scikit-learn scikit-image h5py sureal meson cython \
	&& mkdir /tmp/vmaf \
	&& cd /tmp/vmaf \
	&& git clone https://github.com/Netflix/vmaf.git . \
	&& make \
	&& make install \
        && rm -r /tmp/vmaf


RUN \
	apt-get install -y yasm pkg-config \
	&& mkdir /tmp/ffmpeg \
	&& cd /tmp/ffmpeg \
	&& git clone https://git.ffmpeg.org/ffmpeg.git . \
	&& ./configure --enable-libvmaf --enable-version3 --pkg-config-flags="--static" \
	&& make -j 8 install \
	&& rm -r /tmp/ffmpeg



RUN \
	mkdir -p /home/shared-vmaf

RUN \
        ldconfig
