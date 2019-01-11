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

RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash \
	&& apt-get update && apt-get install -y graphviz ghostscript sox git-lfs \
	&& apt-get clean \
	&& git lfs install \
	&& rm -rf /var/lib/apt/lists/*

RUN git config --global credential.helper cache

RUN mkdir -p /usr/local/src/
WORKDIR /usr/local/src

RUN pip3 install -e git+https://github.com/mycroftai/adapt#egg=adapt-parser

CMD bash

