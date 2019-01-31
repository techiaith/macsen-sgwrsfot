# coding: utf-8
from __future__ import unicode_literals


LOOKUP = {
"chwaraea":"chwarae",
"gerddoriaeth":"cerddoriaeth",
"fiwsig":"miwsig",
"thechnoleg":'technoleg',
"Nghaerdydd":"Caerdydd",
"Mangor":"Bangor",
"Mhwllheli":"Pwllheli",
"Nghaerfyrddin":"Caerfyrddin"
}

LOWER_LOOKUP = dict((k.lower(), v.lower()) for k,v in LOOKUP.items())

def lemmatize(wordform):
    searchform = wordform.lower()
    if searchform in LOWER_LOOKUP:
        return LOWER_LOOKUP.get(searchform)
    else:
        return wordform

def add_inflection(inflection, lemma):
    LOWER_LOOKUP[inflection.lower()] = lemma.lower()

