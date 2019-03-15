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
        skill_response=[]
        context = intent_parser_result.matches
        for key, value in context.items():
            context[key] = context[key].replace("?","")

        hours_key = (h in context.keys() for h in ("hour_morning", "hour_afternoon", "hour_evening"))
        print ("#####################")
        print (context)
        print (hours_key) 
        print ("#####################")
        if hours_key or 'hanner_nos_dydd' in context.keys():
            alarm_time=datetime.datetime.now()
            alarm_time_description=''
            if hours_key:
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
        hour_text=''
        period=''
        hours=0

        if "hour_morning" in context:
            hour_text=context["hour_morning"]
            hours=convert.HOUR_LOOKUP[hour_text]
            period=context["morning_period"]
        elif "hour_afternoon" in context:
            hour_text=context["hour_afternoon"]
            hours=convert.HOUR_LOOKUP[hour_text]
            hours=hours+12
            period=context["afternoon_period"]
        else:
            hour_text=context["hour_evening"]
            hours=convert.HOUR_LOOKUP[hour_text]
            hours=hours+12
            period=context["evening_period"]

        alarm_time_description="%s %s" % (hour_text, period)

        minutes = 0

        alarm_time=alarm_time.replace(hour=hours)
        alarm_time=alarm_time.replace(minute=minutes)

        return alarm_time, alarm_time_description

