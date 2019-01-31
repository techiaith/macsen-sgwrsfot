FROM ubuntu:16.04
MAINTAINER Uned Technolegau Iaith, Prifysgol Bangor University

# Setup Linux base environment
RUN apt-get update \ 
    && apt-get install -q -y \
	libtext-ngrams-perl \
        git \
	cmake \
        locales \
	python3 \ 
	python3-pip \
	python3-dev \
	perl \
        wget \
	curl \
	zlib1g-dev \
	zip \
	vim 

# Set the locale
RUN locale-gen cy_GB.UTF-8
ENV LANG cy_GB.UTF-8  
ENV LANGUAGE cy_GB:en  
ENV LC_ALL cy_GB.UTF-8


RUN mkdir -p /opt/FaNN \
  && cd /opt/FaNN \
  && wget http://downloads.sourceforge.net/project/fann/fann/2.2.0/FANN-2.2.0-Source.zip \
  && unzip FANN-2.2.0-Source.zip \
  && cd FANN-2.2.0-Source/ \
  && cmake . \
  && make install \
  && apt-get install -q -y libfann-dev swig \
  && pip3 install padatious


RUN mkdir -p /opt/padatious
#ADD padatious /opt/padatious

WORKDIR /opt/padatious/
RUN wget http://techiaith.cymru/enwaulleoedd/EnwauCymru/EnwauCymru.txt

# Skills
RUN pip3 install pyowm feedparser



RUN mkdir -p /opt/adapt-api/
WORKDIR /opt/adapt-api

RUN pip3 install -e git+https://github.com/mycroftai/adapt#egg=adapt-parser


CMD bash

