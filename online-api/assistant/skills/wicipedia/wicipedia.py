#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pyowm
import pprint

from dateutil.tz import tzlocal
from datetime import datetime, timedelta

from Skill import Skill
from padatious import IntentContainer



class wicipedia_skill(Skill):

    def __init__(self, root_dir, name, nlp):
        super(wicipedia_skill, self).__init__(root_dir, name, nlp)

        

    def handle(self, intent_parser_result, latitude, longitude):
        skill_response = []

        context = intent_parser_result.matches
        for key, value in context.items():
            context[key] = context[key].replace("?","")


        result = 'Bydd Wicipedia Cymraeg yn medru ateb chi cyn bo hir'

        skill_response.append({
            'title':result,
            'description':'',
            'url':''
        })
        return skill_response
