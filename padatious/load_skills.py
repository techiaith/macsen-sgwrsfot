#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from padatious import IntentContainer

placenames_cy = []


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
           
           print (placename_cy, placename_en, longitude, latitude)


def load_skill_intents(skills_root_dir, skillname):

    skill_intents_root_dir = os.path.join(skills_root_dir, skillname, 'intents')
    skill_intents_container = IntentContainer(skillname + "_cache")

    for intent_file_path in os.listdir(skill_intents_root_dir):
        if intent_file_path.endswith('.intent'):
            intent_name = "intent_" + intent_file_path.replace('.intent', '')
            sentence_examples = [] 
            with open(os.path.join(skill_intents_root_dir, intent_file_path), 'r', encoding='utf-8') as intent_file:
                for sentence_example in intent_file:
                    sentence_examples.append(sentence_example)
            skill_intents_container.add_intent(intent_name, sentence_examples)

    skill_intents_container.train() 

    print (skill_intents_container.calc_intent("Beth yw'r tywydd ym Mhwllheli?")) 


 
if __name__ == "__main__":
    #load_placename_entities('/opt/padatious/EnwauCymru.txt') 
    load_skill_intents('/opt/padatious/skills','tywydd')

