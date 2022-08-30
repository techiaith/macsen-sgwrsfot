#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import datetime

from .nlg import convert

from Skill import Skill
from padatious import IntentContainer


class larwm_skill(Skill):


    def __init__(self, root_dir, name, nlp, active):
        super(larwm_skill, self).__init__(root_dir, name, nlp, active)


    def handle(self, intent_parser_result, latitude, longitude):
        skill_response=[]
        context = intent_parser_result.matches
        for key, value in context.items():
            context[key] = context[key].replace("?","")

        if 'awr' or 'hanner_nos_dydd' in context.keys():
            alarm_time=datetime.datetime.now()
            alarm_time_description=''
            if 'awr' in context.keys():
                alarm_time, alarm_time_description=self.handle_time_with_hours(context)
            elif 'hanner_nos_dydd' in context.keys():
                alarm_time, alarm_time_description=self.handle_mid_time(context)
            
            alarm_time_result = {
                'string': '{:%Y-%m-%d %H:%M%z}'.format(alarm_time),
                'hour':alarm_time.hour,
                'minutes':0
            }

            skill_response.append({
                'title':"Gosod larwm",
                'success':True,
                'description':'Am gosod larwm am %s' % alarm_time_description,
                'alarmtime':alarm_time_result
            })

        else:
            skill_response.append({
                'title':"Gosod larwm",
                'success':False,
                'description':"Methwyd deall am faint o'r gloch mae angen gosod larwm",
                'alarmtime':''
            })

        return skill_response


    def handle_mid_time(self, context):
        alarm_time = datetime.datetime.now()
        hours=convert.HANNER_NOS_DYDD_LOOKUP[context["hanner_nos_dydd"]]
        minutes=0

        alarm_time=alarm_time.replace(hour=hours)
        alarm_time=alarm_time.replace(minute=minutes)
        
        alarm_time_full='%s' % (context["hanner_nos_dydd"])

        return alarm_time, alarm_time_full
      

    def handle_time_with_hours(self, context):
        alarm_time = datetime.datetime.now()

        hours_text=context["awr"]
        hours=convert.HOUR_LOOKUP[hours_text]
        period=context["cyfnod"]
        if period == 'nos' and hours < 5:
            cyfnod='bore'
        elif period != 'bore' and hours < 13:
            hours=hours+12

        alarm_time_description="%s yn %s" % (hours_text, period)

        minutes = 0

        alarm_time=alarm_time.replace(hour=hours)
        alarm_time=alarm_time.replace(minute=minutes)

        return alarm_time, alarm_time_description

