#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Skill import Skill
from padatious import IntentContainer

class golau_skill(Skill):

    def __init__(self, root_dir, name, nlp, active):
        super(golau_skill, self).__init__(root_dir, name, nlp, active)


    def handle(self, intent_parser_result, latitude, longitude):

        skill_response = []
        context = intent_parser_result.matches
        
        print (intent_parser_result.name, context)
        result = 'golau_skill'
        
        nlg_description = ''
        light_state = ''
        room= ''

        if context["ymlaen_i_ffwrdd"]=="i ffwrdd":
            light_state="off"                
        elif context["ymlaen_i_ffwrdd"]=="ymlaen":
            light_state="on"

        if "ystafell" in context:
            room=context["ystafell"]
            if room=="gegin":
                room="cegin"
            nlg_description = "Am roi golau'r %s %s" % (context["ystafell"], context["ymlaen_i_ffwrdd"])
                           
        elif "ystafell_x" in context:
            room=context["ystafell_x"]
            nlg_description = "Am roi'r golau yn yr %s %s" % (context["ystafell_x"], context["ymlaen_i_ffwrdd"])

        #
        skill_response.append({
            'title':result,
            'description':nlg_description,
            'url':'',
            'room':room,
            'light_state':light_state
        })

        return skill_response
