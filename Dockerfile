FROM alpine:latest
LABEL maintainer="@kevinzepeda"

RUN apk update \
 && apk add bash squid 

RUN apk add python3 && apk add py3-pip 

COPY entrypoint.sh /sbin/entrypoint.sh
RUN chmod 755 /sbin/entrypoint.sh

EXPOSE 3128/tcp
ENTRYPOINT ["/sbin/entrypoint.sh"]