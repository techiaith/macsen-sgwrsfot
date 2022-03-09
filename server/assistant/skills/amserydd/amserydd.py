#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Skill import Skill
from padatious import IntentContainer

class amserydd_skill(Skill):

    def __init__(self, root_dir, name, nlp, active):
        super(amserydd_skill, self).__init__(root_dir, name, nlp, active)


    def handle(self, intent_parser_result, latitude, longitude):

        skill_response = []
        context = intent_parser_result.matches
        
        print (intent_parser_result.name, context)
        result = 'Amserydd'
        duration = 0

        nlg_description = ''        

        #
        if "rhan_o_awr" in context:
            if context["rhan_o_awr"] == "awr":
                duration = "3600"
                nlg_description = "Am amseru awr"
            elif context["rhan_o_awr"] == "chwarter awr":
                duration = "900"
                nlg_description = "Am amseru chwarter awr"
            elif context["rhan_o_awr"] == "hanner awr":
                duration = "1800"
                nlg_description = "Am amseru hanner awr"
            if context["rhan_o_awr"] == "dri chwarter awr":
                duration = "2700"
                nlg_description = "Am amseru dri chwarter awr"

        elif "munud" in context or "funud" in context:
            duration = str(self.convert_number_string_to_int(context["munud"]) * 60)
            nlg_description = "Am amseru %s " % context["munud"]

        elif "eiliad" in context:
            duration = str(self.convert_number_string_to_int(context["eiliad"]))
            nlg_description = "Am amseru %s eiliad" % context["eiliad"]
        
        #
        skill_response.append({
            'title':result,
            'description':nlg_description,
            'url':'',
            'duration_length':duration           
        })

        return skill_response


    def convert_number_string_to_int(self, str_number):

        str_number = str_number.replace("munud","")
        str_number = str_number.replace("funud","")
        str_number = str_number.replace("eiliad","")
        str_number = str_number.strip()

        if str_number=="un":
            return 1
        if str_number=="dau" or str_number=="ddwy":
            return 2
        if str_number=="dri" or str_number=="dair":
            return 3
        if str_number=="bedwar" or str_number=="bedair":
            return 4
        if str_number=="bum":
            return 5
        if str_number=="chwech":
            return 6
        if str_number=="saith":
            return 7
        if str_number=="wyth":
            return 8
        if str_number=="naw":
            return 9
        if str_number=="deg" or str_number=="ddeg":
            return 10
        if str_number=="ugain":
            return 20
