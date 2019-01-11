__author__ = 'the-kid89'
"""
A sample program that uses multiple intents and disambiguates by
intent confidence
try with the following:
PYTHONPATH=. python examples/multi_intent_parser.py "what's the weather like in tokyo"
PYTHONPATH=. python examples/multi_intent_parser.py "play some music by the clash"
"""

import json
from pprint import pprint

import sys
from adapt.entity_tagger import EntityTagger

from adapt.tools.text.tokenizer import EnglishTokenizer

from adapt.tools.text.trie import Trie

from adapt.intent import IntentBuilder
from adapt.parser import Parser
from adapt.engine import DomainIntentDeterminationEngine

from cy.tokenizer import WelshTokenizer

tokenizer = WelshTokenizer()
engine = DomainIntentDeterminationEngine()


def loadJsonSkill(json_file_path):
   with open(json_file_path, 'r', encoding='utf-8') as skill_json_file:
      skill_json_data = json.load(skill_json_file)

      print("Loading... " + skill_json_data['domain'])
      engine.register_domain(skill_json_data['domain'], tokenizer=tokenizer)

      for intent_json in skill_json_data['intents']:
          intent_builder = IntentBuilder(intent_json["name"])
          for entity_json in intent_json["entities"]:
              for keyword_json in entity_json["keywords"]:
                  engine.register_entity(keyword_json["keyword"], entity_json["name"], domain=skill_json_data['domain'])

              if entity_json["requirement"]=="require":
                  intent_builder.require(entity_json["name"])
              elif entity_json["requirement"]=="optional":
                  intent_builder.optionally(entity_json["name"])

          intent = intent_builder.build()
          engine.register_intent_parser(intent, domain=skill_json_data['domain'])


def determine_intent(text):
    print ("\n\nTestun: " + text)
    for intent in engine.determine_intent(text):
        print(intent)
        print('\n')


if __name__ == "__main__":
    loadJsonSkill('skill-weather.json')
    loadJsonSkill('skill-music.json')

    if len(sys.argv) > 1:
        determine_intent(' '.join(sys.argv[1:]))
    else:
        determine_intent("Beth yw'r tywydd ym Mangor?")
        determine_intent("Chwaraea fiwsig roc")

