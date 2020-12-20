FROM alpine:latest
LABEL maintainer="@kevinzepeda"

WORKDIR /var/spool/squid

RUN apk update \
 && apk add bash squid \
 && apk add python3 py3-pip \
 && apk -U add ca-certificates openssl

RUN mkdir /etc/block
RUN chmod 755 /etc/block
COPY block_lite /etc/block

RUN mkdir -p /etc/squid_default
RUN chmod 755 -R /etc/squid_default
COPY squid/etc/squid.conf /etc/squid_default/squid.conf

COPY entrypoint.sh /sbin/entrypoint.sh
RUN chmod 755 /sbin/entrypoint.sh

EXPOSE 3128/tcp
ENTRYPOINT ["/sbin/entrypoint.sh"]