#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pyowm

from padatious import IntentContainer

class tywydd_handler:

    def handle(self, intent_parser_result):
        owm = pyowm.OWM('***REMOVED***')

        place = intent_parser_result.matches.get("placename")
        observation = owm.weather_at_place(place)
        
        result ="Dyma'r tywydd gan Open Weather ar gyfer %s \n" % place
        result = result + observation.get_weather().get_status()

        return result

