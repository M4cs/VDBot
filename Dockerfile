FROM python:3.9-slim-buster

WORKDIR /usr/app

RUN apt-get update && apt-get install gcc -y

COPY ./requirements.txt /usr/app/requirements.txt
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

COPY . /usr/app

CMD python -m vdbot