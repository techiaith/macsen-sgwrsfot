#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import jsonpickle

import importlib

from nlp.cy.nlp import NaturalLanguageProcessing


class Brain(object):

    def __init__(self):
        self.skills = dict()
        self.nlp = NaturalLanguageProcessing()

        skills_root_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'skills')
        
        self.load_skill(skills_root_dir, 'tywydd')
        self.load_skill(skills_root_dir, 'newyddion')


    def load_skill(self, skills_root_dir, skillname):
        skill_python_module = importlib.import_module('skills.%s.%s' % (skillname, skillname))
        class_ = getattr(skill_python_module, skillname + '_skill')
        instance = class_(skills_root_dir, skillname, self.nlp)
        self.skills[skillname] = instance

   
    def handle(self, text):
        return self.handle_intent(self.determine_intent(text))


    def handle_intent(self, intent):
        return self.skills[intent.name].handle(intent)


    def determine_intent(self, text):
        best_intent = None
        for key in self.skills.keys():
            intent = self.skills[key].calculate_intent(text)
            if not best_intent:
                 best_intent = intent
            if intent.conf > best_intent.conf:
                 best_intent = intent
        return best_intent 


    def expand_intents(self):
        result = []
        for name in self.skills.keys():
            skill = self.skills.get(name)
            result = result + skill.expand_intents()
        return result


if __name__ == "__main__":

    brain = Brain()
    response = brain.handle(sys.argv[1])
    
    print (jsonpickle.encode(response))

    #print(brain.handle(sys.argv[1]))
    #print('\n'.join(brain.expand_intents()))
