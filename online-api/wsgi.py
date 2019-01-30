#!/usr/bin/env python
import os
import sys
import json
import codecs

import cherrypy
import logging

from adapt.intent import IntentBuilder
from adapt.engine import DomainIntentDeterminationEngine

from cy.nlp.tokenizer import WelshTokenizer

# intent specific...
from cy.intents.python.TywyddBBC import get_bbc_location_id


class AdaptAPI(object):

    def __init__(self):
              
        self.tokenizer = WelshTokenizer()
        self.intent_engine = DomainIntentDeterminationEngine()

        intents_dir = "cy/intents" 
        for intent in os.listdir(intents_dir):
            intent_description_file=os.path.join(intents_dir, intent)
            if not os.path.isdir(intent_description_file):
                self.loadJson(intent_description_file)
 
    def loadJson(self, json_file_path):
        with codecs.open(json_file_path, 'r', encoding='utf-8') as skill_json_file:
            skill_json_data = json.load(skill_json_file)
            cherrypy.log("Loading... " + skill_json_data['domain'])
            self.intent_engine.register_domain(skill_json_data['domain'], tokenizer=self.tokenizer)

            for intent_json in skill_json_data['intents']:
                intent_builder = IntentBuilder(intent_json["name"])
                for entity_json in intent_json["entities"]:
                    for keyword_json in entity_json["keywords"]:
                        self.intent_engine.register_entity(keyword_json["keyword"], entity_json["name"], domain=skill_json_data['domain'])

                    if entity_json["requirement"]=="require":
                        intent_builder.require(entity_json["name"])
                    elif entity_json["requirement"]=="optional":
                        intent_builder.optionally(entity_json["name"])

                    intent = intent_builder.build()
                    self.intent_engine.register_intent_parser(intent, domain=skill_json_data['domain'])

    @cherrypy.expose
    def index(self):
        return "determine_intent/?text=....."

    def post_process_intent(self, intent):
        if intent["intent_type"] == "WeatherIntent":
            if "Location" in intent:
                cherrypy.log("Adding extra metadata bbc location id to intent")
                intent["bbc_location_id"] = get_bbc_location_id(intent["Location"])

        return intent


    @cherrypy.expose
    def determine_intent(self, text, **kwargs):
        cherrypy.log("determining_intent:  '%s'" % text)
        try:
            if not text:
                raise ValueError("'text' missing")
        except ValueError as e:
            return "ERROR: %s" % str(e)

        json_result = ''

        intents = []

        for intent in self.intent_engine.determine_intent(text):
            intents.append(self.post_process_intent(intent))

        if len(intents)>0:
            json_result = json.dumps(intents[0])

        cherrypy.log('intent result %s ' % json_result)
        return json_result


cherrypy.config.update({
    'environment': 'production',
    'log.screen': False,
    'response.stream': True,
    'log.error_file': 'adapt-api.log',
})

cherrypy.tree.mount(AdaptAPI(), '/')
application = cherrypy.tree

