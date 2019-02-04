#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import importlib

from nlp.cy.nlp import NaturalLanguageProcessing

SKILLS_ROOT_DIR = '/opt/skills-online-api/assistant/skills'

class Brain(object):
    def __init__(self):
        self.skills = dict()
        self.nlp = NaturalLanguageProcessing()

        self.load_skill(SKILLS_ROOT_DIR, 'tywydd')
        self.load_skill(SKILLS_ROOT_DIR, 'newyddion')

    def load_skill(self, skills_root_dir, skillname):
        skill_python_module = importlib.import_module('skills.%s.%s' % (skillname, skillname))
        class_ = getattr(skill_python_module, skillname + '_skill')
        instance = class_(skills_root_dir, skillname, self.nlp)
        self.skills[skillname] = instance

   
    def handle(self, text):
        return self.handle_intent(self.determine_intent(text))


    def handle_intent(self, intent):
        return self.skills[intent.name.replace("intent_", "")].handle(intent)


    def determine_intent(self, text):
        best_intent = None
        for key in self.skills.keys():
            intent = self.skills[key].calculate_intent(text)
            if not best_intent:
                 best_intent = intent
            if intent.conf > best_intent.conf:
                 best_intent = intent
        return best_intent 


