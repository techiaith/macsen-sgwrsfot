#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import requests
import xml.etree.ElementTree as ET

import datetime

from .timezonedb.apikey import TIMEZONEDB_API_KEY

from Skill import Skill
from padatious import IntentContainer

misoedd = ['Ionawr', 'Chwefror', 'Mawrth', 'Ebrill', 'Mai', 'Mehefin', 'Gorffennaf', 'Awst', 'Medi', 'Hydref', 'Tachwedd', 'Rhagfyr']

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

        datetime_object = datetime.datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S')
     
        result = ''   
        if 'gloch_keyword' in context:
            result += 'Mae hi nawr yn %s' % str(datetime_object.time())
        elif 'dyddiad_keyword' in context:
            result += 'Dyddiad heddiw yw %s %s %s' % (
                misoedd[datetime_object.date().month-1],
                str(datetime_object.date().day),
                str(datetime_object.date().year))

        skill_response.append({
            'title':result,
            'description':'',
            'url':''
        })

        return skill_response
