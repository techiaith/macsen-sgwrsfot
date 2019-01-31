#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pyowm
from padatious import IntentContainer

class tywydd_handler:

    def handle(self, intent_parser_result):

        owm = pyowm.OWM('***REMOVED***')

        place = intent_parser_result.matches.get("placename")
        observation = owm.weather_at_place(place)
        print (observation)

        w=observation.get_weather()
        print (w)
        print (w.get_temperature('celsius'))

        
