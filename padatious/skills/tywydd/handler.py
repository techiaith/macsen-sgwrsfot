#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pyowm

from padatious import IntentContainer


class tywydd_handler:


    def __init__(self):
        self.placenames = {}
        self.initialize_placenames()


    def handle(self, intent_parser_result):
        owm = pyowm.OWM('***REMOVED***')
        context = intent_parser_result.matches

        response = "Dyma'r tywydd gan OpenWeather ar gyfer {placename} "
        result = response.format(**context)

        place = intent_parser_result.matches.get("placename")
        observation = owm.weather_at_place(place)
        result = result + observation.get_weather().get_status()

        return result


    def preprocess(self, placename):
        placename = placename.strip()
        if ',' in placename:
            prep = placename[placename.index(','):]
            placename = placename.replace(prep, '')
            placename = prep + ' ' + placename
            placename = placename.replace(',', '').lstrip().rstrip()
        return placename


    def initialize_placenames(self):
        with open('/data/EnwauCymru.txt', 'r', encoding='utf-8') as placename_file:
           for placename_data in placename_file:
               placename_cy = self.preprocess(placename_data[0:51])
               if placename_cy in self.placenames.keys():
                   continue
               placename_en = self.preprocess(placename_data[51:102])
               longitude = self.preprocess(placename_data[102:153])
               latitude = self.preprocess(placename_data[153:])

               self.placenames[placename_cy] = (placename_en, longitude, latitude)

