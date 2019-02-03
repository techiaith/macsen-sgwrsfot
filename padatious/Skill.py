#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import importlib

from padatious import IntentContainer

#from nlp.cy.nlp import NaturalLanguageProcessing

skill_handlers = dict()
skill_intent_parsers = dict()


class Skill(object):

    def __init__(self, root_dir, name, nlp):
        self._root_dir = root_dir
        self._name = name
        self._nlp = nlp
        self._intent_container = self.initialize_intent_parser()


    def initialize_intent_parser(self):
        intents_container = IntentContainer("%s_cache" % self._name)
        intents_root_dir = os.path.join(self._root_dir, self._name, 'intents')
        entities_root_dir = os.path.join(self._root_dir, self._name, 'entities')

        # load intents
        for intent_file_path in os.listdir(intents_root_dir):
            if intent_file_path.endswith('.intent'):
                intent_name = "intent_%s" % intent_file_path.replace('.intent', '')
                intents_container.add_intent(intent_name, self.get_skill_file_content(os.path.join(intents_root_dir, intent_file_path)))

        # load entities 
        for entities_file_path in os.listdir(entities_root_dir):
            if entities_file_path.endswith('.entities'):
                entity_type = entities_file_path.replace('.entities', '')
                intents_container.add_entity(entity_type, self.get_skill_file_content(os.path.join(entities_root_dir, entities_file_path)))

        intents_container.train(debug=True, single_thread=False, timeout=3600)
        return intents_container


    def calculate_intent(self, text):
        text = self._nlp.preprocess(text)
        return self._intent_container.calc_intent(text)


    def get_skill_file_content(self, skill_file_path):
        content_array = []
        with open(skill_file_path, 'r', encoding='utf-8') as skill_file:
            for entry in skill_file:
                content_array.append(entry)
        return content_array

    def handle(self, intent):
        pass 
