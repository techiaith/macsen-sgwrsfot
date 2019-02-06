#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pyowm
import pprint

from Skill import Skill

from .owm.translate import Translator

from padatious import IntentContainer

class tywydd_skill(Skill):

    def __init__(self, root_dir, name, nlp):
        super(tywydd_skill, self).__init__(root_dir, name, nlp)

        self.placenames = {}
        self.initialize_placenames()
        self.translator=Translator()
        

    def handle(self, intent_parser_result):
        owm = pyowm.OWM('***REMOVED***')
        context = intent_parser_result.matches
        context["placename"] = context["placename"].capitalize()
        response = []
        try:
            if context["placename"] in self.placenames:
                response = self.get_weather_for_placename_in_wales(owm, context)
            else:
                response = self.get_weather_for_placename(owm, context)
        except :
            template = "Mae'n ddrwg gen i, ond dwi methu estyn y tywydd ar gyfer {placename}\n"
            response = template.format(**context)

        return response


    def get_weather_for_placename_in_wales(self, owm, context):

        skill_response = []

        placename_en, longitude, latitude = self.placenames[context["placename"]]
        longitude = float(longitude)
        latitude = float(latitude)
        observation = owm.weather_at_coords(latitude, longitude)

        w = observation.get_weather()
        l = observation.get_location()
        context["city"] = l.get_name()
        context["country"] = l.get_country() 

        title_template = ''
        if context["city"]==context["placename"] or context["city"]==placename_en:
            title_template = "Dyma'r tywydd presenol gan OpenWeather ar gyfer {placename} {country}\n"
        else:
            title_template = "Dyma'r tywydd presenol gan OpenWeather ar gyfer {city} ger {placename} {country}\n"
        
        temperature = w.get_temperature('celsius').get("temp")
        status_cy = self.translator.translate('status', w.get_status())
        description = "Mae hi'n %s gyda'r tymheredd yn %s gradd celcius\n" % (status_cy, temperature)

        skill_response.append({
            'title' : title_template.format(**context), 
            'description' : description, 
            'url' : ''
        }) 

        forecast = owm.three_hours_forecast_at_coords(latitude, longitude).get_forecast()

        next_temperatures, next_status, next_time = [], [], []
        for next_weather in forecast:
            next_temperatures.append(next_weather.get_temperature('celsius').get('temp'))
            next_status.append(next_weather.get_status())
            next_time.append(next_weather.get_reference_time(timeformat='iso'))


        skill_response.append({
            'title' : '',
            'description' : "Am {} bydd hi'n {} gyda'r tymheredd yn {} gradd celsius\n".format(
                           next_time[0],
                           self.translator.translate('status', next_status[0]), 
                           next_temperatures[0]),
            'url' : ''}
        )

        skill_response.append({
            'title' : '',
            'description' : "Ac yna am {} bydd hi'n {} gyda'r tymheredd yn {} gradd celsius\n".format(
                           next_time[1],
                           self.translator.translate('status', next_status[1]), 
                           next_temperatures[1]),
            'url' : ''} 
        )
 
        return skill_response

   

    def get_weather_for_placename(self, owm, context):

        skill_response = []

        observation = owm.weather_at_place(context["placename"])
        w = observation.get_weather()
        l = observation.get_location()
        context["city"] = l.get_name()
        context["country"] = l.get_country() 

        title_template = ''
        if context["city"]==context["placename"] or context["city"]==placename_en:
            title_template = "Dyma'r tywydd presenol gan OpenWeather ar gyfer {placename} {country}\n"
        else:
            title_template = "Dyma'r tywydd presenol gan OpenWeather ar gyfer {city} ger {placename} {country}\n"


        temperature = w.get_temperature('celsius').get("temp")
        status_cy = self.translator.translate('status', w.get_status())
        description = "Mae hi'n %s gyda'r tymheredd yn %s gradd celcius" % (status_cy, temperature)

        skill_response.append({
            'title' : title_template.format(**context), 
            'description' : description
        })

        return skill_response


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

                # placenames are not added, because of training limitations, to intent parsing 
                # self._intent_container.add_entity('placename', list(self.placenames.keys()))


    def get_additional_entities(self, entity_name): 
       result = []
       if entity_name == 'placename':
           for p in sorted(self.placenames.keys()):
               result.append(p)
               mutations = self._nlp.get_lemmatization().get_mutations(p)
               for m in mutations:
                   result.append(m.capitalize())
       else:
           return []

       return result

