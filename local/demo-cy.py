__author__ = 'the-kid89'
"""
A sample program that uses multiple intents and disambiguates by
intent confidence
try with the following:
PYTHONPATH=. python examples/multi_intent_parser.py "what's the weather like in tokyo"
PYTHONPATH=. python examples/multi_intent_parser.py "play some music by the clash"
"""

import json
import sys
from adapt.entity_tagger import EntityTagger

from adapt.tools.text.tokenizer import EnglishTokenizer

from adapt.tools.text.trie import Trie
from adapt.intent import IntentBuilder
from adapt.parser import Parser
from adapt.engine import DomainIntentDeterminationEngine

from cy.tokenizer import WelshTokenizer

tokenizer = WelshTokenizer()

#tagger = EntityTagger(trie, tokenizer)
#parser = Parser(tokenizer, tagger)

engine = DomainIntentDeterminationEngine()

engine.register_domain('DomainWeather', tokenizer=tokenizer)
engine.register_domain('DomainMusic', tokenizer=tokenizer)

# define vocabulary
weather_keyword = [
    "tywydd"
]
for wk in weather_keyword:
    engine.register_entity(wk, "WeatherKeyword", domain='DomainWeather')

locations = [
    "Bangor",
    "Caerdydd",
    "Caerfyrddin",
    "Pwllheli"
]
for loc in locations:
    engine.register_entity(loc.lower(), "WeatherLocation", domain='DomainWeather')

# structure intent
weather_intent = IntentBuilder("WeatherIntent")\
    .require("WeatherKeyword")\
    .optionally("WeatherLocation")\
    .build()



# define music vocabulary
music_verbs = [
    "chwarae"
]
for mv in music_verbs:
    engine.register_entity(mv, "MusicVerb", domain='DomainMusic')

music_types = [
    "roc",
    "Cymraeg",
    "araf",
    "dawnsio"
]
for mt in music_types:
    engine.register_entity(mt, "MusicType", domain='DomainMusic')

music_keywords = [
    "cerddoriaeth",
    "miwsig"
]
for mk in music_keywords:
    engine.register_entity(mk, "MusicKeyword", domain='DomainMusic')


music_intent = IntentBuilder("MusicIntent")\
    .require("MusicVerb")\
    .require("MusicKeyword")\
    .optionally("MusicType")\
    .build()

engine.register_intent_parser(weather_intent, domain='DomainWeather')
engine.register_intent_parser(music_intent, domain='DomainMusic')

def determine_intent(text):
    for intent in engine.determine_intent(text):
        print("\n** Intent: ** \n") 
        print(intent)
        print('\n\n')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        determine_intent(' '.join(sys.argv[1:]))
    else:
        determine_intent("Beth yw'r tywydd ym Mangor?")
        determine_intent("Chwaraea fiwsig roc") 

