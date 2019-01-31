#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import importlib

from padatious import IntentContainer

placenames_cy = []

skills_repository = dict()


def preprocess(placename):
    placename = placename.rstrip()
    if ',' in placename:
        prep = placename[placename.index(','):]
        placename = placename.replace(prep, '')
        placename = prep + ' ' + placename
        placename = placename.replace(',', '').lstrip().rstrip()
    return placename


def load_placename_entities(placename_file_path):
    with open(placename_file_path, 'r', encoding='utf-8') as placename_file:
       for placename_data in placename_file:

           placename_cy = preprocess(placename_data[0:51])
           placename_en = preprocess(placename_data[51:102])

           longitude = placename_data[102:153].rstrip()
           latitude = placename_data[153:].rstrip() 


def load_skill_intents(skills_root_dir, skillname):

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
    skills_repository[skillname] = skill_intents_container


def determine_intent(text):
    best_intent = None
    for key, intent_container in skills_repository.items():
       intent = intent_container.calc_intent(text)
       if not best_intent:
           best_intent = intent
       if intent.conf > best_intent.conf:
           best_intent = intent

    return best_intent 


def handle_intent(intent):
    skill_python_module = importlib.import_module('skills.%s.handler' % intent.name.replace("intent_",""))
    class_ = getattr(skill_python_module, intent.name.replace("intent_", "") + "_handler")
    instance = class_()
    print (instance.handle(intent))

 
if __name__ == "__main__":
    #load_placename_entities('/opt/padatious/EnwauCymru.txt') 
    
    #print (skill_intents_container.calc_intent("Beth yw'r tywydd ym Mhwllheli?")) 
    SKILLS_ROOT_DIR='/opt/padatious/src/skills'  

    load_skill_intents(SKILLS_ROOT_DIR, 'tywydd')
    load_skill_intents(SKILLS_ROOT_DIR, 'newyddion')

    handle_intent(determine_intent("Beth yw'r newyddion chwaraeon?"))
    handle_intent(determine_intent("Sut mae'r tywydd yn Helsinki?"))

