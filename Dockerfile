FROM python:3-buster

RUN ln -snf /usr/share/zoneinfo/Europe/Moscow /etc/localtime && echo Europe/Moscow > /etc/timezone

ENV HTTPS_PROXY http://proxy-server.sovcombank.group:3128
ENV HTTP_PROXY http://proxy-server.sovcombank.group:3128
ENV https_proxy http://proxy-server.sovcombank.group:3128
ENV http_proxy http://proxy-server.sovcombank.group:3128
ENV NO_PROXY "127.0.0.1,localhost,.sovcombank.group,minio,.sovcombank.ru,coroot-clickhouse,coroot-clickhouse.coroot-clickhouse"

RUN groupadd -g 1000 python
RUN useradd -s /bin/bash -g python -u 1000 -g 1000 python

RUN mkdir -p /app/lib && chown -R python:python /app
WORKDIR /app/lib

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV PYTHONPATH=/app/lib

COPY --chown=1000:1000 ./app /app/lib/

USER python

ENTRYPOINT ["kopf", "run", "--liveness=http://0.0.0.0:8080/healthz"]
CMD ["main.py"]