#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import jsonpickle

import importlib

from RecordingsDatabase import RecordingsDatabase

from nlp.cy.nlp import NaturalLanguageProcessing
from nlp.cy.cysill import CysillArleinAPI

from skills_assistant_tasks import initialize_recordings_database_task

class Brain(object):

    def __init__(self):
        self.skills = dict()
        self.nlp = NaturalLanguageProcessing()

        skills_root_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'skills')

        self.load_skill(skills_root_dir, 'tywydd')
        self.load_skill(skills_root_dir, 'newyddion')
        self.load_skill(skills_root_dir, 'amser')
        self.load_skill(skills_root_dir, 'spotify')
        self.load_skill(skills_root_dir, 'larwm')

        self.mysql_db = RecordingsDatabase()
        self.mysql_db.initialize()

        initialize_recordings_database_task.delay(self.expand_intents(), os.path.join(skills_root_dir, 'ignore.dict'))


    def load_skill(self, skills_root_dir, skillname):
        skill_python_module = importlib.import_module('skills.%s.%s' % (skillname, skillname))
        class_ = getattr(skill_python_module, skillname + '_skill')
        instance = class_(skills_root_dir, skillname, self.nlp)
        self.skills[skillname] = instance


    def get_unrecorded_sentence(self, uid):
        return self.mysql_db.select_random_unrecorded_sentence(uid)


    def handle(self, text, latitude=0.0, longitude=0.0):
        # Bangor, Gwynedd 
        if latitude==0.0 and longitude==0.0:
            latitude=53.2167738950777
            longitude=-4.14310073720948

        handler_key, intent = self.determine_intent(text)
        skill_result=self.handle_intent(handler_key, intent, latitude, longitude)
        return intent.name, skill_result


    def handle_intent(self, handler_key, intent, latitude, longitude):
        return self.skills[handler_key].handle(intent, latitude, longitude)


    def determine_intent(self, text):
        best_intent = None
        best_handler = None
        best_score = 0.0

        for key in self.skills.keys():
            adapt_confidence, intent = self.skills[key].calculate_intent(text)
            print ( key, adapt_confidence, str(intent.conf))
            score=adapt_confidence*intent.conf
            if score > best_score:
                best_intent = intent
                best_handler = key
                best_score=score

        return best_handler, best_intent


    def expand_intents(self, include_additional_entities=False):
        result = {}
        for name in self.skills.keys():
            skill = self.skills.get(name)
            result[name] = skill.expand_intents(include_additional_entities)
        print (result)
        return result


if __name__ == "__main__":

    brain = Brain()
    #print('\n'.join(brain.expand_intents()))

    response = brain.handle(sys.argv[1])
    print (jsonpickle.encode(response))

