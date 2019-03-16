#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import requests

from .api.search import search_artist
from Skill import Skill
from padatious import IntentContainer


class spotify_skill(Skill):

    def __init__(self, root_dir, name, nlp):
        super(spotify_skill, self).__init__(root_dir, name, nlp)


    def handle(self, intent_parser_result, latitude, longitude):

        # chwaraea.cerddoriaeth {'artist': 'Anweledig'}
        skill_response = []
        context = intent_parser_result.matches
        for key, value in context.items():
            context[key] = context[key].replace("?","")

        data=search_artist(context["artist"])
        items=data['artists']['items']
        if len(items) > 0:
            for b in items:
                skill_response.append({
                    'title':b["name"],
                    'description':'',
                    'url':b["uri"]})
        else:
            skill_response.append({
                'title':'',
                'description':'Methwyd dod o hyd i fiwsig gan %s ar Spotify' % context["artist"],
                'url':''})

        return skill_response

