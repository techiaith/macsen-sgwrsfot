#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import importlib

import itertools
from string import Formatter

from adapt.intent import IntentBuilder
from adapt.engine import DomainIntentDeterminationEngine

from padatious import IntentContainer
from padatious.util import expand_parentheses



class EntitiesDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'


class Skill(object):


    def __init__(self, root_dir, name, nlp):
        self._root_dir = root_dir
        self._name = name
        self._nlp = nlp

        self._intents_container = None
        self._adapt_intent_engine = None

        self.initialize_intent_parser()


    def get_name(self):
        return self._name


    def initialize_intent_parser(self):
       
        self._intents_container = IntentContainer("%s_cache" % self._name)

        self._adapt_intent_engine = DomainIntentDeterminationEngine()
        self._adapt_intent_engine.register_domain(self._name)

        for intent_name, intent_file_path in self.get_intent_names():
            print ("IntentBuilder: %s, %s" % (intent_name, intent_file_path))         
            intent_builder = IntentBuilder(intent_name)
            for intent_name, intent_example_sentences_array in self.intent_training_file_content(intent_file_path, 'intent'):
                #print ("add intent %s, %s" % (intent_name, intent_example_sentences_array))
                self._intents_container.add_intent(intent_name, intent_example_sentences_array)

            for entity_name, entities_array in self.intent_training_file_content(intent_file_path, 'entities'):
                #print ("add entity %s, %s " % (entity_name, entities_array))
                self._intents_container.add_entity(entity_name, entities_array)
                if entity_name.endswith("_keyword"):
                    for k in entities_array:
                        print ("add keyword %s to %s" % (k, intent_name))
                        self._adapt_intent_engine.register_entity(k, 'keyword', domain=self._name)
                 
            intent=intent_builder.require('keyword').build()
            self._adapt_intent_engine.register_intent_parser(intent, domain=self._name) 
 
        self._intents_container.train()


    def get_skill_file_content(self, skill_file_path):
        content_array = []
        with open(skill_file_path, 'r', encoding='utf-8') as skill_file:
            for entry in skill_file:
                content_array.append(entry.strip())
        return content_array


    def get_intent_names(self):
        intent_root_file_path=os.path.join(self._root_dir, self._name, 'intents')
        for intent_name in os.listdir(intent_root_file_path):
            intent_file_path=os.path.join(intent_root_file_path, intent_name)
            yield intent_name, intent_file_path


    def intent_training_file_content(self, artefacts_root_dir, artefact_file_extension):
        for artefact_file_path in os.listdir(artefacts_root_dir):
            if artefact_file_path.endswith('.' + artefact_file_extension):
                artefact_name = artefact_file_path.replace('.' + artefact_file_extension, '')
                artefact_file_lines = self.get_skill_file_content(os.path.join(artefacts_root_dir, artefact_file_path))
                yield artefact_name, artefact_file_lines
        

    def expand_intents(self, include_additional_entities=False):
        # load entities first in the file and build a dictionary
        result = []
        entities_dict = dict()

        for intent_name, intent_file_path in self.get_intent_names():

            for entity_type, entities_array in self.intent_training_file_content(intent_file_path, 'entities'):
                entities_dict[entity_type]=entities_array
 
            # load intents again from file
            for intent_type, intent_array in self.intent_training_file_content(intent_file_path, 'intent'):
                for line in intent_array:
                    line_tokens = self._nlp.tokenization.tokenize(line)
                    expanded = expand_parentheses(line_tokens)
                    for sentence_tokens in expanded:
                        sentence = self._nlp.tokenization.detokenize(sentence_tokens)
                        fieldnames = [fname for _, fname, _, _ in Formatter().parse(sentence) if fname]
                        fields_dict = dict()
                        for fieldname in fieldnames:
                            if fieldname in entities_dict:
                                fields_dict[fieldname]=entities_dict[fieldname].copy()
                            else:
                                 if include_additional_entities:
                                     field_values = self.get_additional_entities(fieldname)
                                     if len(field_values) > 0:
                                         fields_dict[fieldname]=field_values

                        if len(fields_dict) > 0:
                            keys, values = zip(*fields_dict.items())
                            permutations = [dict(zip(keys, v)) for v in itertools.product(*values)]
                            for p in permutations:
                                entities_dict_permutation = EntitiesDict(p)
                                result.append(sentence.format(**entities_dict_permutation))
                        else:
                            result.append(sentence)
        return result 


    def get_additional_entities(self, fieldname):
        return [] 


    def calculate_intent(self, text):
        text = self._nlp.preprocess(text)
        print ("evaluating: %s with adapt:" % text)
        
        adapt_result = self._adapt_intent_engine.determine_intent(text)
        for a in adapt_result:
            print (a)

        print ("evaluating: %s with padatious:" % text)
        padatious_result = self._intents_container.calc_intent(text)
        print (padatious_result)

        return padatious_result


    def handle(self, intent, latitude, longitude):
        pass 


