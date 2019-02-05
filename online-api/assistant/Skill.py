#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import importlib

import itertools
from string import Formatter

from padatious import IntentContainer
from padatious.util import expand_parentheses


class Skill(object):

    def __init__(self, root_dir, name, nlp):
        self._root_dir = root_dir
        self._name = name
        self._nlp = nlp

        self._intent_container = self.initialize_intent_parser()


    def get_name(self):
        return self._name


    def initialize_intent_parser(self):
        intents_container = IntentContainer("%s_cache" % self._name)

        # load intents
        for intent_name, intents_array in self.padatious_training_file_content('intents'):
            intents_container.add_intent(intent_name, intents_array)

        # load entities 
        for entity_name, entities_array in self.padatious_training_file_content('entities'):
            intents_container.add_entity(entity_name, entities_array)
        
        intents_container.train()
        return intents_container


    def padatious_training_file_content(self, artefact_type):
        artefacts_root_dir = os.path.join(self._root_dir, self._name, artefact_type)
        for artefact_file_path in os.listdir(artefacts_root_dir):
            if artefact_file_path.endswith('.' + artefact_type):
                artefact_name = artefact_file_path.replace('.' + artefact_type, '')
                artefact_file_lines = self.get_skill_file_content(os.path.join(artefacts_root_dir, artefact_file_path))
                yield artefact_name, artefact_file_lines
        

    def expand_intents(self):
        # load entities first in the file and build a dictionary
        result = []
        entities_dict = dict()
        for entity_type, entities_array in self.padatious_training_file_content('entities'):
            entities_dict[entity_type]=entities_array
 
        # load intents again from file
        for intent_type, intent_array in self.padatious_training_file_content('intents'):
            for line in intent_array:
                line_tokens = self._nlp.tokenization.tokenize(line)
                expanded = expand_parentheses(line_tokens)
                for sentence_tokens in expanded:
                    sentence = self._nlp.tokenization.detokenize(sentence_tokens)
                    fieldnames = [fname for _, fname, _, _ in Formatter().parse(sentence) if fname]
                    fields_dict = dict()
                    for fieldname in fieldnames:
                        if fieldname in entities_dict:
                             fields_dict[fieldname]=entities_dict[fieldname]
                        else:
                             field_values = self.get_additional_entities(fieldname)
                             if len(field_values) > 0:
                                 fields_dict[fieldname]=field_values

                    if len(fields_dict) > 0:
                        keys, values = zip(*fields_dict.items())
                        permutations = [dict(zip(keys, v)) for v in itertools.product(*values)]
                        for p in permutations:
                            result.append(sentence.format(**p))
                    else:
                        result.append(sentence)

        return result 

    def get_additional_entities(self, fieldname):
        return [] 


    def calculate_intent(self, text):
        text = self._nlp.preprocess(text)
        return self._intent_container.calc_intent(text)


    def get_skill_file_content(self, skill_file_path):
        content_array = []
        with open(skill_file_path, 'r', encoding='utf-8') as skill_file:
            for entry in skill_file:
                content_array.append(entry.strip())
        return content_array


    def handle(self, intent):
        pass 
