#!/bin/bash
mkdir -p /data/corpus/clips

# create corpus.txt
python3 /opt/padatious/src/Brain.py -s > /data/corpus/corpus.txt

#rsync clips
rsync -rvt /recordings/ /data/corpus/clips
