############################################################
# Dockerfile to build Python WSGI Application Containers
# Based on Ubuntu/Debia
############################################################


# Set the base image to Ubuntu
FROM python:3.8

MAINTAINER Stefan Hesse

ADD requirements.txt /home/flask/app/requirements.txt

RUN pip install -r /home/flask/app/requirements.txt
ADD . /home/flask/app/backend


ENV PYTHONPATH="/home/flask/app/"


WORKDIR /home/flask/app/backend

CMD python main.py