FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN mkdir /src
RUN mkdir /project
RUN mkdir /report

COPY requirements.txt /src/

RUN pip3 install --upgrade pip \
    && pip3 install -r src/requirements.txt \
    && apt-get update -qq \
    && apt-get install postgresql -y \
    && apt-get install vim -y \
	&& apt-get install -y git x11vnc

WORKDIR /src/project
