#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import importlib

from padatious import IntentContainer

from nlp.cy.tokenizer import WelshTokenizer

skill_handlers = dict()
skill_intent_parsers = dict()


def load(skills_root_dir, skillname):
    load_intent_parser(skills_root_dir, skillname)
    load_skill_handler(skillname)


def load_skill_handler(skillname):
    skill_python_module = importlib.import_module('skills.%s.handler' % skillname)
    class_ = getattr(skill_python_module, skillname + '_handler')
    instance = class_()
    #if hasattr(instance, 'get_lemmatization'):
    #    instance.get_lemmatization()

    skill_handlers[skillname]=instance

    #skill_python_module = importlib.import_module('skills.%s.handler' % intent.name.replace("intent_",""))
    #class_ = getattr(skill_python_module, intent.name.replace("intent_", "") + "_handler")
    #instance = class_()
    #print (instance.handle(intent))


def load_intent_parser(skills_root_dir, skillname):

    skill_intents_container = IntentContainer(skillname + "_cache")

    skill_intents_root_dir = os.path.join(skills_root_dir, skillname, 'intents')
    skill_entities_root_dir = os.path.join(skills_root_dir, skillname, 'entities')

    for intent_file_path in os.listdir(skill_intents_root_dir):
        if intent_file_path.endswith('.intent'):
            intent_name = "intent_" + intent_file_path.replace('.intent', '')
            sentence_examples = [] 
            with open(os.path.join(skill_intents_root_dir, intent_file_path), 'r', encoding='utf-8') as intent_file:
                for sentence_example in intent_file:
                    sentence_examples.append(sentence_example)
            skill_intents_container.add_intent(intent_name, sentence_examples)

    for entities_file_path in os.listdir(skill_entities_root_dir):
        if entities_file_path.endswith('.entities'):
            entity_name = entities_file_path.replace('.entities','')
            entities = []
            with open(os.path.join(skill_entities_root_dir, entities_file_path), 'r', encoding='utf-8') as entities_file:
                for entity in entities_file:
                    entities.append(entity)
            skill_intents_container.add_entity(entity_name, entities)

    skill_intents_container.train() 
    skill_intent_parsers[skillname] = skill_intents_container


    
def handle_intent(intent):
    print (skill_handlers[intent.name.replace("intent_","")].handle(intent))


def determine_intent(text, tokenizer):

    best_intent = None
    text = tokenizer.tokenize(text, True)
    text = tokenizer.detokenize(text)

    for key, intent_container in skill_intent_parsers.items():
       intent = intent_container.calc_intent(text)
       if not best_intent:
           best_intent = intent
       if intent.conf > best_intent.conf:
           best_intent = intent

    return best_intent 



 
if __name__ == "__main__":
    #load_placename_entities('/opt/padatious/EnwauCymru.txt') 
    
    SKILLS_ROOT_DIR='/opt/padatious/src/skills'  

    load(SKILLS_ROOT_DIR, 'tywydd')
    load(SKILLS_ROOT_DIR, 'newyddion')

    tokenizer = WelshTokenizer()
    tokenizer.add_inflection_to_lemmatizer("Mhorthmadog","Porthmadog")


    #handle_intent(determine_intent("Beth yw'r newyddion chwaraeon?", tokenizer))
    #handle_intent(determine_intent("Sut mae'r tywydd ym Mhorthmadog?", tokenizer))
    handle_intent(determine_intent(sys.argv[1], tokenizer)) 
