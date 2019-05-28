FROM ubuntu

RUN apt-get update -qq

RUN \
	apt-get install -y build-essential git make \
	&& mkdir /tmp/vmaf \
	&& cd /tmp/vmaf \
	&& git clone https://github.com/Netflix/vmaf.git . \
	&& cd ptools \
	&& make \
	&& cd ../wrapper \
	&& make \
	&& cd .. \
	&& make install \
	&& rm -r /tmp/vmaf


RUN \
	apt-get install -y yasm pkg-config \
	&& mkdir /tmp/ffmpeg \
	&& cd /tmp/ffmpeg \
	&& git clone https://git.ffmpeg.org/ffmpeg.git . \
	&& ./configure --enable-libvmaf --enable-version3 \
	&& make -j 8 install \
	&& rm -r /tmp/ffmpeg



RUN \
	mkdir -p /home/shared-vmaf
