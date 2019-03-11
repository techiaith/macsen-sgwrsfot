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
        alarm_time = datetime.datetime.now()
        alarm_time_description=''
        context = intent_parser_result.matches
        for key, value in context.items():
            context[key] = context[key].replace("?","")

        if 'hour' in context.keys():
            alarm_time, alarm_time_description=self.handle_time_with_hours(context)
        elif 'hanner_nos_dydd' in context.keys():
            alarm_time, alarm_time_description=self.handle_mid_time(context)

        alarm_time_result = {
            'string': '{:%Y-%m-%d %H:%M%z}'.format(alarm_time),
            'hour':alarm_time.hour,
            'minutes':alarm_time.minute
        }
        
        skill_response.append({
            'title':"Gosod larwm",
            'description':'Am gosod larwm am %s' % alarm_time_description,
            'alarmtime':alarm_time_result
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
        hours=convert.HOUR_LOOKUP[context["hour"]]
        hours=convert.convertTo24hr(hours, context["day_period"])

        if "i_wedi" in context:
            if context["i_wedi"]=='i':
                hours=hours-1

        alarm_time_description=''
        if "hanner_chwarter" in context and "i_wedi" in context:
            alarm_time_description='%s %s %s %s' % (context["hanner_chwarter"], context["i_wedi"], context["hour"], context["day_period"])
            minutes = convert.convertHannerChwarter(context["hanner_chwarter"], context["i_wedi"])
        else:
            alarm_time_description="%s %s" % (context["hour"], context["day_period"])
            minutes = 0

        alarm_time=alarm_time.replace(hour=hours)
        alarm_time=alarm_time.replace(minute=minutes)

        return alarm_time, alarm_time_description

