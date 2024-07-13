FROM ubuntu:20.04

RUN apt-get update \
    && apt-get -y install libpq-dev
RUN apt-get install python3 python3-pip -y
RUN pip3 install --upgrade pip
WORKDIR /app

COPY ./requirements.txt ./

RUN pip3 install -r requirements.txt

COPY ./ /app

CMD python3 run.py