FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y wine64 && mkdir -p /malware && mkdir /logs

WORKDIR /malware

ENTRYPOINT ["wine"]
CMD ["--version"]
