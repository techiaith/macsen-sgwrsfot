#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import datetime

from .nlg import convert

from Skill import Skill
from padatious import IntentContainer


class larwm_skill(Skill):

    def __init__(self, root_dir, name, nlp):
        super(larwm_skill, self).__init__(root_dir, name, nlp)


    def handle(self, intent_parser_result, latitude, longitude):

        skill_response = []
        print (intent_parser_result.sent)
        context = intent_parser_result.matches
        for key, value in context.items():
            context[key] = context[key].replace("?","")

        print (intent_parser_result.name, context)

        hour=convert.HOUR_LOOKUP[context["hour"]]
        hour=convert.convertTo24hr(hour, context["day_period"])
        if context["i_wedi"]=='i':
            hour=hour-1

        print (context["hanner_chwarter"])

        minutes = convert.convertHannerChwarter(context["hanner_chwarter"], context["i_wedi"])

        alarm_time = datetime.datetime.now()
        alarm_time.hour=hour
        alarm_time.minutes=minutes


        skill_response.append({
            'title':"Am gosod larwm",
            'description':'',
            'alarmtime':
            'url':''
        })

        return skill_response

