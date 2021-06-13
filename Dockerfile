FROM python:3.7-slim

RUN mkdir -m 777 -p /source/hit-maker
ADD requirements.txt /source/hit-maker
RUN pip install -r /source/hit-maker/requirements.txt

ADD ./ /source/hit-maker
WORKDIR /source/hit-maker
