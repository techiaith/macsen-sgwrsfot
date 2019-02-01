#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pyowm
import pprint
from padatious import IntentContainer


class tywydd_handler:


    def __init__(self):
        self.placenames = {}
        self.initialize_placenames()


    def handle(self, intent_parser_result):
        owm = pyowm.OWM('***REMOVED***')
        context = intent_parser_result.matches

        context["placename"] = context["placename"].capitalize()
        placename_en, longitude, latitude = self.placenames[context.get("placename")]
        longitude = float(longitude)
        latitude = float(latitude)

        observation = owm.weather_at_coords(latitude, longitude)

        w = observation.get_weather()
        l = observation.get_location()
        context["city"] = l.get_name()
        context["country"] = l.get_country() 

        response = ''
        if context["city"]==context["placename"] or context["city"]==placename_en:
            response = "Dyma'r tywydd presenol gan OpenWeather ar gyfer {placename} {country}\n"
        else:
            response = "Dyma'r tywydd presenol gan OpenWeather ar gyfer {city} ger {placename} {country}\n"

        result = response.format(**context)

        temperature = w.get_temperature('celsius').get("temp")
        description = "Mae hi'n %s gyda'r tymheredd yn %s gradd celcius" % (w.get_status().lower(), temperature)
        result = result + description

        #forecast = owm.three_hours_forecast_at_coords(latitude, longitude)
        #pprint.pprint (forecast.get_forecast().to_XML())

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

