FROM ubuntu:22.04

RUN dpkg --add-architecture i386 && \
	apt update && \
	apt install -y wine64 wine32 curl

WORKDIR /malware

COPY run.sh /run.sh
RUN chmod +x /run.sh

ENTRYPOINT ["/run.sh"]
