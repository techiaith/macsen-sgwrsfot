#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .lemmatization import Lemmatization
from .tokenization import Tokenization

class NaturalLanguageProcessing(object):

    def __init__(self):
        self.tokenization = Tokenization()
        self.lemmatization = Lemmatization()
      

    def get_lemmatization(self):
        return self.lemmatization


    def get_tokenization(self):
        return self.tokenization


    def preprocess(self, text):
        toks = self.tokenization.tokenize(text)
        lemma_toks = [] 
        for t in toks:
            lemma_toks.append(self.lemmatization.lemmatize(t))
        return self.tokenization.detokenize(lemma_toks)
         

