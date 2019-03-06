#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import requests

from Skill import Skill
from padatious import IntentContainer


class spotify_skill(Skill):

    def __init__(self, root_dir, name, nlp):
        super(spotify_skill, self).__init__(root_dir, name, nlp)


    def handle(self, intent_parser_result, latitude, longitude):

        # chwaraea.cerddoriaeth {'artist_neu_band': 'Anweledig', 'cerddoriaeth_keyword': 'fiwsig'}
        skill_response = []
        context = intent_parser_result.matches
        for key, value in context.items():
            context[key] = context[key].replace("?","")

        print (intent_parser_result.name, context)

        result = context["artist_neu_band"]

        skill_response.append({
            'title':result,
            'description':'',
            'url':''
        })

        return skill_response

