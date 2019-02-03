#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .lemmatizer import Lemmatizer
from .tokenizer import Tokenizer

class NaturalLanguageProcessing(object):

    def __init__(self):
        self.tokenizer = Tokenizer()
        self.lemmatizer = Lemmatizer()


    def get_lemmatizer(self):
        return self.lemmatizer


    def get_tokenizer(self):
        return self.tokenizer


    def preprocess(self, text):
        toks = self.tokenizer.tokenize(text)
        lemma_toks = [] 
        for t in toks:
            lemma_toks.append(self.lemmatizer.lemmatize(t))
        return self.tokenizer.detokenize(lemma_toks)
          
