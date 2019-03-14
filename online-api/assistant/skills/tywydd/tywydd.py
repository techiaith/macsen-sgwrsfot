#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pyowm
import pprint

from dateutil.tz import tzlocal
from datetime import datetime, timedelta

from Skill import Skill

from .owm.translate import Translator
from .owm.apikey import OWM_API_KEY

from padatious import IntentContainer


class tywydd_skill(Skill):

    def __init__(self, root_dir, name, nlp):
        super(tywydd_skill, self).__init__(root_dir, name, nlp)

        self.placenames = {}
        self.initialize_placenames()
        self.translator=Translator()
        

    def handle(self, intent_parser_result, latitude, longitude):
         
        context = intent_parser_result.matches
        for key, value in context.items():
            context[key] = context[key].replace("?","")

        observation, forecasts = self.get_weather_data(context, latitude, longitude)
        
        if "time_future" in context.keys():
            return self.generate_weather_report_for_tomorrow(context, observation, forecasts)
        else:
            return self.generate_weather_report_for_today(context, observation, forecasts)
      

    def get_weather_data(self, context, latitude, longitude):
        ## get data from OpenWeatherMap API...
        if "placename" in context.keys():
            context["placename"] = context["placename"].capitalize()
            if context["placename"] in self.placenames:
                placename_en, longitude, latitude = self.placenames[context["placename"]]
                longitude = float(longitude)
                latitude = float(latitude)
                observation = self.api_get_weather_at_coords(float(latitude), float(longitude))
                forecasts = self.api_get_forecast_at_coords(float(latitude), float(longitude))
            else:
                observation = self.api_get_weather_for_placename(context["placename"])
                forecasts = self.api_get_forecast_for_placename(context["placename"])
        else:
            observation = self.api_get_weather_at_coords(float(latitude), float(longitude))
            forecasts = self.api_get_forecast_at_coords(float(latitude), float(longitude))
        return observation, forecasts

    def api_get_weather_at_coords(self, latitude, longitude):
        owm = pyowm.OWM(OWM_API_KEY)
        observation = owm.weather_at_coords(latitude, longitude)
        return observation


    def api_get_weather_for_placename(self, placename):
        owm = pyowm.OWM(OWM_API_KEY)
        observation = owm.weather_at_place(placename)
        return observation


    def api_get_forecast_for_placename(self, placename):
        owm = pyowm.OWM(OWM_API_KEY)
        forecast = owm.three_hours_forecast(placename).get_forecast()
        return forecast


    def api_get_forecast_at_coords(self, latitude, longitude):
        owm = pyowm.OWM(OWM_API_KEY)
        forecast = owm.three_hours_forecast_at_coords(latitude, longitude).get_forecast()
        return forecast


    def generate_weather_report_for_today(self, context, observation, forecasts):
        placename_en = ''
        skill_response = []

        ## current weather...
        w = observation.get_weather()
        l = observation.get_location()
        context["city"] = l.get_name()
        context["country"] = l.get_country() 

        title_template = ''
        if "placename" in context.keys():
            if context["city"]==context["placename"] or context["city"]==placename_en:
                title_template = "Dyma'r tywydd presenol gan OpenWeatherMap ar gyfer {placename}."
            else:
                title_template = "Dyma'r tywydd presenol gan OpenWeatherMap ar gyfer {city} ger {placename}."
        else:
            title_template = "Dyma'r tywydd presennol gan OpenWeatherMap ar gyfer {city}."

        status_cy = self.translator.generate_phrase('status', w.get_status())
        temperature = float(w.get_temperature('celsius').get("temp"))
        description_template = "Mae %s gyda'r tymheredd yn %s gradd Celsius"
        if temperature < 0:
            description_template = description_template + " o dan y rhewbwynt"
            temperature = abs(temperature)
        description = description_template % (status_cy, self._nlp.tokenization.round_float_token(temperature))

        #
        skill_response.append({
            'title' : title_template.format(**context), 
            'description' : description + ".", 
            'url' : ''
        }) 

        ## forecast contains 40 observations at three hours intervals. 
        forecast_weather_count=0
        for forecast_weather in forecasts:
            if forecast_weather_count > 1:
                break

            temperature = forecast_weather.get_temperature('celsius').get('temp')
            temperature = self._nlp.tokenization.round_float_token(temperature)

            status = forecast_weather.get_status()
            status = self.translator.generate_phrase('status', status)

            time = forecast_weather.get_reference_time(timeformat='iso')
            time = self._nlp.tokenization.datetime_token_to_hours_words(time)
    
            if forecast_weather_count==0:
                description_template = "Am {} bydd {} gyda'r tymheredd yn {} gradd Celsius"
            else:
                description_template = "Ac yna am {} bydd {} gyda'r tymheredd yn {} gradd Celsius"

            if temperature < 0:
                description_template = description_template + " o dan y rhewbwynt"
                temperature = abs(temperature)

            description_template = description_template + "."

            skill_response.append({
                'title' : '',
                'description' : description_template.format(time, status, temperature),
                'url' : ''}
            )
            forecast_weather_count += 1

        return skill_response


    def generate_weather_report_for_tomorrow(self, context, observation, forecasts):
        placename_en=''
        skill_response = []

        w = observation.get_weather()
        l = observation.get_location()
        context["city"] = l.get_name()
        context["country"] = l.get_country()

        title_template = ''
        if "placename" in context.keys():
            if context["city"]==context["placename"] or context["city"]==placename_en:
                title_template = "Dyma tywydd yfory gan OpenWeatherMap ar gyfer {placename}."
            else:
                title_template = "Dyma tywydd yfory gan OpenWeatherMap ar gyfer {city} ger {placename}."
        else:
            title_template = "Dyma tywydd yfory gan OpenWeatherMap ar gyfer {city}."


        skill_response.append({
            'title' : title_template.format(**context),
            'description' : "",
            'url' : ""
        })

        ## forecast contains 40 observations at three hours intervals. 
        time_now = datetime.now(tzlocal())
        time_tomorrow = time_now + timedelta(days=1)
        forecast_weather_count=0
        for forecast_weather in forecasts:

            time = forecast_weather.get_reference_time(timeformat='iso')
            dt = self._nlp.tokenization.token_to_datetime(time)
            if dt < time_tomorrow:
                continue 

            if forecast_weather_count > 1:
                break
            
            time = self._nlp.tokenization.datetime_token_to_hours_words(time)

            temperature = forecast_weather.get_temperature('celsius').get('temp')
            temperature = self._nlp.tokenization.round_float_token(temperature)

            status = forecast_weather.get_status()
            status = self.translator.generate_phrase('status', status)

            if forecast_weather_count==0:
                description_template = "Fory am {} bydd {} gyda'r tymheredd yn {} gradd Celsius"
            else:
                description_template = "Ac yna am {} bydd {} gyda'r tymheredd yn {} gradd Celsius"

            if temperature < 0:
                description_template = description_template + " o dan y rhewbwynt"
                temperature = abs(temperature)

            description_template = description_template + "."

            skill_response.append({
                'title' : '',
                'description' : description_template.format(time, status, temperature),
                'url' : ''}
            )
            forecast_weather_count += 1

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

