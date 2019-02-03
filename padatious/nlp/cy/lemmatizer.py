#!/usr/bin/env python3
# coding: utf-8
from __future__ import unicode_literals

class Lemmatizer(object):
    def __init__(self):
        self.lookup = {}
 
    def lemmatize(self, wordform):
        searchform = wordform.lower()
        if searchform in self.lookup:
            return self.lookup.get(searchform)
        else:
            return wordform

    def add_inflection(self, inflection, lemma):
        self.lookup[inflection.lower()] = lemma.lower() 

