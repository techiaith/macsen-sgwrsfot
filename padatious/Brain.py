#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import importlib

from nlp.cy.nlp import NaturalLanguageProcessing

skills = dict()


def load_skill(skills_root_dir, skillname, nlp):
    skill_python_module = importlib.import_module('skills.%s.%s' % (skillname, skillname))
    class_ = getattr(skill_python_module, skillname + '_skill')
    instance = class_(skills_root_dir, skillname, nlp)
    skills[skillname] = instance

    
def handle_intent(intent):
    print (skills[intent.name.replace("intent_","")].handle(intent))


def determine_intent(text):

    best_intent = None

    for key in skills.keys():
       intent = skills[key].calculate_intent(text)
       if not best_intent:
           best_intent = intent
       if intent.conf > best_intent.conf:
           best_intent = intent

    return best_intent 


if __name__ == "__main__":
    
    SKILLS_ROOT_DIR='/opt/padatious/src/skills'  

    nlp = NaturalLanguageProcessing()

    load_skill(SKILLS_ROOT_DIR, 'tywydd', nlp)
    load_skill(SKILLS_ROOT_DIR, 'newyddion', nlp)

    handle_intent(determine_intent(sys.argv[1])) 
