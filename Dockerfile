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
        mysql-client \
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

# padatious
RUN mkdir -p /opt/FaNN \
  && cd /opt/FaNN \
  && wget http://downloads.sourceforge.net/project/fann/fann/2.2.0/FANN-2.2.0-Source.zip \
  && unzip FANN-2.2.0-Source.zip \
  && cd FANN-2.2.0-Source/ \
  && cmake . \
  && make install \
  && apt-get install -q -y libfann-dev swig \
  && pip3 install padatious

# adapt
RUN pip3 install -e git+https://github.com/mycroftai/adapt#egg=adapt-parser

RUN rm -rf /var/lib/apt/lists/*

RUN mkdir -p /data
WORKDIR /data
RUN wget http://techiaith.cymru/enwaulleoedd/EnwauCymru/EnwauCymru.txt

RUN mkdir -p /opt/padatious
WORKDIR /opt/padatious/

# Skills
RUN pip3 install pyowm feedparser jsonpickle pytz python-dateutil PyMySQL spotipy wikipedia

CMD bash

