#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

class Translator:

    def __init__(self):
       self._translations = dict()
       self.initialize() 


    def translate(self, own_field, text):
        text = text.lower()
        try:
            return self._translations[own_field][text].strip()
        except:
            return text

    def generate_phrase(self, own_field, text):
        text = text.lower()
        print (text, own_field)
        try:
            translation = self._translations[own_field][text].strip()
            if own_field is 'status':
                if text == 'clear':
                   return "hi'n glir"
                else:
                   return "yna %s" % translation
        except:
            return text


    def initialize(self):
        trans_files_dir = os.path.dirname(os.path.realpath(__file__))
        for trans_file in os.listdir(trans_files_dir):
            if trans_file.endswith('.cy'):
               field = trans_file.replace(".cy","")
               self._translations[field] = self.read_file(os.path.join(trans_files_dir, trans_file))


    def read_file(self, file_path):
        translations = dict()
        with open(file_path, 'r', encoding='utf-8') as trans_file:
            for trans in trans_file:
                en,cy = tuple(trans.split('|'))
                en = en.lower()
                cy = cy.lower()
                translations[en]=cy
        return translations 
            
