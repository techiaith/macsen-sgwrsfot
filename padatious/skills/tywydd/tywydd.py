#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pyowm
import pprint

from Skill import Skill

from padatious import IntentContainer


class tywydd_skill(Skill):

    def __init__(self, root_dir, name, nlp):
        super(tywydd_skill, self).__init__(root_dir, name, nlp)

        self.placenames = {}
        self.initialize_placenames()



    def handle(self, intent_parser_result):
        owm = pyowm.OWM('301745d853a8d421b86a37680f5bef2d')
        context = intent_parser_result.matches
        context["placename"] = context["placename"].capitalize()
        response = ''
        try:
            if context["placename"] in self.placenames:
                response = self.get_weather_for_placename_in_wales(owm, context)
            else:
                response = self.get_weather_for_placename(owm, context)
        except:
            template = "Mae'n ddrwg gen i, ond dwi methu estyn y tywydd ar gyfer {placename}\n"
            response = template.format(**context)
 
        #forecast = owm.three_hours_forecast_at_coords(latitude, longitude)
        #pprint.pprint (forecast.get_forecast().to_XML())

        return response


    def get_weather_for_placename_in_wales(self, owm, context):

        placename_en, longitude, latitude = self.placenames[context["placename"]]
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

        return result


    def get_weather_for_placename(self, owm, context):
        observation = owm.weather_at_place(context["placename"])
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
        if os.path.isfile('/data/EnwauCymru.txt'):
            with open('/data/EnwauCymru.txt', 'r', encoding='utf-8') as placenames_file:
                for _ in range(2):
                  next(placenames_file)

                for placename_data in placenames_file:
                    placename_cy = self.preprocess(placename_data[0:51])
                    if placename_cy in self.placenames.keys():
                        continue
                    placename_en = self.preprocess(placename_data[51:102])
                    longitude = self.preprocess(placename_data[102:153])
                    latitude = self.preprocess(placename_data[153:])

                    self.placenames[placename_cy] = (placename_en, longitude, latitude)
                    self._nlp.get_lemmatization().add_lemma(placename_cy)

                self._intent_container.add_entity('placename', list(self.placenames.keys()))

