FROM python:3.9-slim-buster

WORKDIR /usr/app

COPY ./requirements.txt /usr/app/requirements.txt

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

COPY . /usr/app

CMD python -m vdbot