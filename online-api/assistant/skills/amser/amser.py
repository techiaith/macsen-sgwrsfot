#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import requests
import xml.etree.ElementTree as ET

from dateutil.tz import tzlocal
from datetime import datetime, timedelta

from .timezonedb.apikey import TIMEZONEDB_API_KEY

from Skill import Skill
from padatious import IntentContainer


class amser_skill(Skill):

    def __init__(self, root_dir, name, nlp):
        super(amser_skill, self).__init__(root_dir, name, nlp)


    def handle(self, intent_parser_result, latitude, longitude):

        skill_response = []
         
        context = intent_parser_result.matches
        for key, value in context.items():
            context[key] = context[key].replace("?","")

        print (context)

        url = "http://api.timezonedb.com/v2.1/get-time-zone"
        payload = {
            'key' : TIMEZONEDB_API_KEY,
            'by':'position',
            'lat':latitude, 
            'lng':longitude
        }

        r = requests.get(url, params=payload)
        responseXml = ET.fromstring(r.text)
        datetime_string = responseXml.find('formatted').text

        datetime_string_components = datetime_string.split()
        date_string = datetime_string_components[0].strip()
        time_string = datetime_string_components[1].strip()
        time_string = time_string[:-3] 
     
        result = ''   
        if 'gloch_keyword' in context:
            result += 'Mae hi nawr yn %s' % time_string
        elif 'dyddiad_keyword' in context:
            result += 'Dyddiad heddiw yw %s' % date_string

        skill_response.append({
            'title':result,
            'description':'',
            'url':''
        })

        return skill_response
