#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import jsonpickle

import importlib

from nlp.cy.nlp import NaturalLanguageProcessing

class Brain(object):

    def __init__(self, online=True):
        self.skills = dict()
        self.nlp = NaturalLanguageProcessing()

        skills_root_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'skills')

        self.load_skill(skills_root_dir, 'tywydd')
        self.load_skill(skills_root_dir, 'newyddion')
        self.load_skill(skills_root_dir, 'amser')
        self.load_skill(skills_root_dir, 'spotify')
        self.load_skill(skills_root_dir, 'larwm')
        self.load_skill(skills_root_dir, 'wicipedia')

        if online:
            from RecordingsDatabase import RecordingsDatabase
            from skills_assistant_tasks import initialize_recordings_database_task
            
            self.mysql_db = RecordingsDatabase()
            self.mysql_db.initialize()
            initialize_recordings_database_task.delay(self.expand_skills())


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
            latitude=53.2303869
            longitude=-4.1299242

        print (latitude, longitude)

        best_key, best_intent = self.determine_intent(text)
        if best_intent: 
            skill_result=self.handle_intent(best_key, best_intent, latitude, longitude)
            return best_intent.name, skill_result
        else:
            return '', None


    def handle_intent(self, handler_key, intent, latitude, longitude):
        return self.skills[handler_key].handle(intent, latitude, longitude)


    def determine_intent(self, text):
        best_intent = None
        best_handler = ''
        best_score = 0.0

        for key in self.skills.keys():
            adapt_confidence, intent = self.skills[key].calculate_intent(text)
            print ( key, adapt_confidence, str(intent))
            score=adapt_confidence*intent.conf
            if score > best_score:
                best_intent = intent
                best_handler = key
                best_score=score

        return best_handler, best_intent


    def expand_skills(self, include_additional_entities=False):
        result = {}
        for name in self.skills.keys():
            skill = self.skills.get(name)
            result[name] = skill.expand_intents(include_additional_entities)
        return result


if __name__ == "__main__":

    brain = Brain(online=False)

    skills = brain.expand_skills()
    for skill in skills:
        for intent in skills[skill]:
            print (skill, intent)
            for sentence in skills[skill][intent]:
                print (skill, intent, sentence)

    if len(sys.argv) > 1:
        response = brain.handle(sys.argv[1])
        print (jsonpickle.encode(response))

