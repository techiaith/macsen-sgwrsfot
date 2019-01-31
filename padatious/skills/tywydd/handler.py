#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pyowm

from padatious import IntentContainer

class tywydd_handler:

    def handle(self, intent_parser_result):
        owm = pyowm.OWM('301745d853a8d421b86a37680f5bef2d')
        context = intent_parser_result.matches

        response = "Dyma'r tywydd gan OpenWeather ar gyfer {placename} "
        result = response.format(**context)

        place = intent_parser_result.matches.get("placename")
        observation = owm.weather_at_place(place)
        result = result + observation.get_weather().get_status()

        return result

