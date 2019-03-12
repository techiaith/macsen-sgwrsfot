#!/usr/bin/env python3
import os
import sys
import json
from urllib import request
from urllib.parse import urlencode

from .cysill_arlein_apikey import CYSILL_ARLEIN_APIKEY
from .tokenization import Tokenization

API_LANG = "cy"
API_URL = "https://api.techiaith.org/cysill/v1/?"


class CysillArleinAPI(object):

    def __init__(self):
        self.tokenization=Tokenization()
        self.ignore_dictionary = set()


    def add_word_to_ignore(self, word):
        tokens=self.tokenization.tokenize(word)
        for t in tokens:
            self.ignore_dictionary.add(t)


    def add_words_to_ignore(self, words):
        for w in words:
            self.add_word_to_ignore(w)


    def save_ignore_words(self, ignore_dictionary_file_path):
        with open(ignore_dictionary_file_path, 'w', encoding='utf-8') as ignore_file:
            ignore_file.write('\n'.join(sorted(self.ignore_dictionary)))


    def open_ignore_words(self, ignore_dictionary_file_path):
        if os.path.exists(ignore_dictionary_file_path):
            with open(ignore_dictionary_file_path, 'r', encoding='utf-8') as ignore_file:
                self.ignore_dictionary = set(l.strip() for l in ignore_file.read().split('\n'))


    def get_errors(self, text):
        errors=[] 
        params = {
            'api_key': CYSILL_ARLEIN_APIKEY.encode('utf-8'),
            'lang': API_LANG.encode('utf-8'),
            'text': text.encode('utf-8')
        }
        url = API_URL + urlencode(params)
        response = request.urlopen(url)
        response = json.loads(response.read().decode('utf-8'))
        if not response['success']:
            # Gwall gyda'r galwad API
            # something went wrong with the API call
            error_messages = u'\n'.join(response['errors'])
            raise ValueError(error_messages)

        all_errors=response['result']
        for error in all_errors:
            if error["isSpelling"]:
                spelling_error=text[error['start']:error['start'] + error['length']]
                if spelling_error in self.ignore_dictionary:
                    continue
            errors.append(error)

        return errors


if __name__== "__main__":
    c=CysillArleinAPI()
    print(c.get_errors(sys.argv[1]))
