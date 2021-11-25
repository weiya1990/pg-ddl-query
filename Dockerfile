FROM docker.io/uroybd/python3-psycopg2-alpine:3.7
MAINTAINER weiya 1830624909@qq.com
WORKDIR /opt/python
RUN mkdir -p /opt/python/etc
ADD ddl-sync.py start.py
ADD db.conf etc/db.conf
ENV CONFIG_DIR=/opt/python/etc
CMD ["python", "-u", "start.py"]
