#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import requests
import json

from Skill import Skill
from padatious import IntentContainer


class clic_skill(Skill):

    def __init__(self, root_dir, name, nlp, active):
        super(clic_skill, self).__init__(root_dir, name, nlp, active)

    def handle(self, intent_parser_result, latitude, longitude):
        skill_response = []

        context = intent_parser_result.matches
        for key, value in context.items():
            context[key] = context[key].replace("?", "")

        search = ''
        clic_page_url = 'https://www.s4c.cymru/clic/'

        if "rhaglen" in context:
            search = context["rhaglen"]

        response = json.loads(requests.get(
            "https://www.s4c.cymru/df/search?lang=c&q=%s" % search).text)
        
        if search == "newyddion":
            search = "newyddion s4c"

        valid_title = 0
        for result in response["progs"]:
            if result["series_title"].lower() == search.lower():
                break
            valid_title += 1

        if len(response["progs"]) > 0:
            series_title = response["progs"][valid_title]["series_title"]
            programme_title = response["progs"][valid_title]["programme_title"]
            short_billing = response["progs"][valid_title]["short_billing"]
            programme_id = response["progs"][valid_title]["programme_id"]

            skill_response.append({
                'title': series_title + (" " + programme_title if programme_title else ""),
                'description': short_billing,
                'url': 'https://www.s4c.cymru/clic/programme/%s' % programme_id,
            })

        return skill_response
