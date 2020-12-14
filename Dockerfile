FROM alpine:latest
LABEL maintainer="@kevinzepeda"

ENV SQUID_CACHE_DIR=/var/spool/squid \
    SQUID_LOG_DIR=/var/log/squid 


RUN apk update \
 && apk add bash squid 
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip3 install sqlalchemy 

COPY /squid/etc/squid.conf /etc/squid/squid.conf

RUN mkdir /var/spool//squid
COPY block /var/spool//squid/
COPY entrypoint.sh /sbin/entrypoint.sh
RUN chmod 755 /sbin/entrypoint.sh
RUN chmod 755 -R /var/spool//squid
RUN chmod +x /var/spool//squid/app.py
WORKDIR /var/spool//squid/

EXPOSE 3128/tcp
ENTRYPOINT ["/sbin/entrypoint.sh"]
