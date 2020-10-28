#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pyowm
import pprint

import wikipedia
from wikipedia import PageError

from Skill import Skill
from padatious import IntentContainer


class wicipedia_skill(Skill):

    def __init__(self, root_dir, name, nlp, active):
        super(wicipedia_skill, self).__init__(root_dir, name, nlp, active)


    def handle(self, intent_parser_result, latitude, longitude):
        skill_response = []

        context = intent_parser_result.matches
        for key, value in context.items():
            context[key] = context[key].replace("?","")

        search = ''

        if "pwnc" in context:
            search = context["pwnc"]

        if "personpresenol" in context:
            search = context["personpersonol"]

        if "persongorffenol" in context:
            search = context["persongorffenol"]

        result = 'Does dim byd yn Wicipedia ynghylch %s' % search
        result = 'Does dim byd yn Wicipedia ynghylch %s' % search
        page_url = 'http://cy.wikipedia.org/wiki/' + search.replace(" ","_")

        if len(search) > 0:
            wikipedia.set_lang("cy")
            result = wikipedia.summary(search, sentences=2)
            page = wikipedia.page(search)
            page_url = page.url

        skill_response.append({
            'title':result,
            'description':'',
            'url':page_url
        })
        
        return skill_response
