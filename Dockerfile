FROM ubuntu:16.04
MAINTAINER Uned Technolegau Iaith, Prifysgol Bangor University

# Setup Linux base environment
RUN apt-get update \ 
    && apt-get install -q -y \
	libtext-ngrams-perl \
        git \
	python3 \ 
	python3-pip \
	python3-dev \
	perl \
        wget \
	curl \
	zlib1g-dev \
	zip \
	vim 


RUN mkdir -p /opt/adapt-api/
WORKDIR /opt/adapt-api

RUN pip3 install -e git+https://github.com/mycroftai/adapt#egg=adapt-parser

CMD bash

