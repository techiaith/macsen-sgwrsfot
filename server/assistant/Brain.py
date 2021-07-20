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
        self.load_skill(skills_root_dir, 'clic')

        if online:
            from RecordingsDatabase import RecordingsDatabase
            from skills_assistant_tasks import initialize_recordings_database_task, initialize_skills_database_task
            
            self.mysql_db = RecordingsDatabase()
            self.mysql_db.initialize()

            initialize_recordings_database_task.delay(self.expand_skills())
            initialize_skills_database_task.delay(self.list_skills())
           
 

    def load_skill(self, skills_root_dir, skillname, active=True):
        try:
            skill_python_module = importlib.import_module('skills.%s.%s' % (skillname, skillname))
            class_ = getattr(skill_python_module, skillname + '_skill')
            instance = class_(skills_root_dir, skillname, self.nlp, active)
            self.skills[skillname] = instance
        except ModuleNotFoundError as err:
            print ("Skill %s not loaded" % skillname)
            print (err)



    def list_skills(self):
        skills = [] 
        for key in self.skills.keys():
            skills.append((key, self.skills[key].is_active()))
        return skills


    def get_unrecorded_sentence(self, uid):
        return self.mysql_db.select_random_unrecorded_sentence(uid)


    def handle(self, text, latitude=0.0, longitude=0.0):
        # Bangor, Gwynedd 
        if latitude==0.0 and longitude==0.0:
            latitude=53.2303869
            longitude=-4.1299242

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

    if len(sys.argv) > 1:
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("-t", "--text")
        parser.add_argument("-s", "--sentences", action='store_true')
        args = parser.parse_args()

        if args.text is not None:
            response = brain.handle(args.text)
            print (jsonpickle.encode(response))
        elif args.sentences is not None:
            response = brain.expand_skills(include_additional_entities=False)
            for skill in response:
                for intent in response[skill]:
                    for sentence in response[skill][intent]: 
                        if len(sentence)==0:
                            continue
                        if '{' in sentence and '}' in sentence:
                            continue
                        print (sentence)
        else:
            print ("Unknown")
    else:
        print ("Expecting -t or -s")

