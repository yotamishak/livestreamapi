FROM ubuntu:19.04

MAINTAINER Yotam Ishak "yotamishak@gmail.com"

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD gunicorn -b 127.0.0.1:5000 quickflash:app