# coding: utf-8
from __future__ import unicode_literals


LOOKUP = {
"chwaraea":"chwarae",
"gerddoriaeth":"cerddoriaeth",
"fiwsig":"miwsig",
"Nghaerdydd":"Caerdydd",
"Mangor":"Bangor",
"Mhwllheli":"Pwllheli",
"Nghaerfyrddin":"Caerfyrddin"
}

LOWER_LOOKUP = dict((k.lower(), v.lower()) for k,v in LOOKUP.items())

def lemmatize(wordform):
    if wordform in LOWER_LOOKUP:
        return LOWER_LOOKUP.get(wordform).lower()
    else:
        return wordform

