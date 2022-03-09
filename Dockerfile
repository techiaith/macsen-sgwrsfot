FROM ubuntu:20.04
MAINTAINER Uned Technolegau Iaith, Prifysgol Bangor University

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/London

RUN apt-get update \
 && apt-get install -y -qq \
	tzdata git supervisor python3 python3-pip python3-dev \
        cmake wget curl locales vim zip zlib1g-dev \
        rabbitmq-server \
 && pip3 install --upgrade pip setuptools


# Set the locale
RUN locale-gen cy_GB.UTF-8
ENV LANG cy_GB.UTF-8  
ENV LANGUAGE cy_GB:en  
ENV LC_ALL cy_GB.UTF-8


# Gosod padatious / Install Padartious
RUN cd /opt && git clone https://github.com/libfann/fann.git FaNN \
  && cd /opt/FaNN \
  && git checkout tags/2.2.0 \
  && cmake . \
  && make install \
  && apt-get install -q -y libfann-dev swig \
  && pip3 install padatious \
  && rm -rf /var/lib/apt/lists/*

# Skills
RUN mkdir -p /opt/skills-server
ADD server /opt/skills-server

WORKDIR /opt/skills-server

RUN pip3 install -r requirements.txt 
ENV PYTHONPATH="${PYTHONPATH}:/opt/skills-server/assistant"

# estyn data defnyddiol ar gyfer rhai sgiliau / 
# fetch some useful data for some of the skills.
RUN mkdir -p /data
WORKDIR /data
RUN wget http://techiaith.cymru/enwaulleoedd/EnwauCymru/EnwauCymru.txt

WORKDIR /opt/skills-server

EXPOSE 8008

CMD ["/bin/bash", "-c", "/opt/skills-server/start.sh"]

