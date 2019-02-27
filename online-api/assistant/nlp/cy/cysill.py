#!/usr/bin/env python3
import json
from urllib import request
from urllib.parse import urlencode

from .cysill_arlein_apikey import CYSILL_ARLEIN_APIKEY

API_LANG = "cy"
API_URL = "https://api.techiaith.org/cysill/v1/?"


class CysillArleinAPI(object):

    def __init__(self):
        pass

    def get_errors(self, text):
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
    
        return response['result']

