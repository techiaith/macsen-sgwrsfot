#!/usr/bin/env python3
# coding: utf-8
from __future__ import unicode_literals

class Lemmatization(object):

    def __init__(self):
        self.lookup = {}

 
    def lemmatize(self, wordform):
        searchform = wordform.lower()
        if searchform in self.lookup:
            return self.lookup.get(searchform)
        else:
            return wordform


    def add_inflection(self, inflection, lemma):
        if inflection.lower() not in self.lookup.keys():
            if lemma == inflection:
                return
            #print ("added %s => %s to lemmatization" % (inflection, lemma))
            self.lookup[inflection.lower()] = lemma.lower() 


    def add_lemma(self, lemma):
        self.add_inflection(self.soft_mutate(lemma.lower()), lemma.lower())
        self.add_inflection(self.nasal_mutate(lemma.lower()), lemma.lower())
        self.add_inflection(self.aspirate_mutate(lemma.lower()), lemma.lower())
        #self.add_inflection(self.h_prothesise(lemma.lower()), lemma.lower())


    def get_mutations(self, lemma):
        result = []

        if lemma.lower() != self.soft_mutate(lemma.lower()):
            result.append(self.soft_mutate(lemma.lower()))

        if lemma.lower() != self.nasal_mutate(lemma.lower()):
            result.append(self.nasal_mutate(lemma.lower()))

        if lemma.lower() != self.aspirate_mutate(lemma.lower()):
            result.append(self.aspirate_mutate(lemma.lower()))

        return result


    def soft_mutate(self, word):
        mutable_letters = set(("b", "c", "d", "g", "ll", "p", "m", "rh", "t"))
        soft_map = [("b", "f"), ("ch", "ch"), ("c", "g"), ("dd", "dd"), ("d", "dd"), ("g", ""),
                    ("ll", "l"), ("ph", "ph"), ("p", "b"), ('m', 'f'), ("rh", "r"), ("th", "th"), ("t", "d")]
        for mutable_letter in mutable_letters:
            if word.startswith(mutable_letter):            
                for mutation in soft_map:
                    if word.startswith(mutation[0]):
                        if mutation[0] not in ["g"]:
                            mutated_word = mutation[1] + word[(len(mutation[0])):]
                        elif mutation[0] in ["g"]:
                            mutated_word = word[1:]
                        return mutated_word
        return word


    def nasal_mutate(self, word):
        mutable_letters = set(("b", "c", "d", "g", "p", "t"))
        nasal_map = [("b", "m"), ("ch", "ch"), ("c", "ngh"), ("dd", "dd"), ("d", "n"), ("g", "ng"), ("p", "mh"), ("g", "ng"), ("th", "th"), ("t", "nh")]
        for mutable_letter in mutable_letters:
            if word.startswith(mutable_letter):            
                for mutation in nasal_map:
                    if word.startswith(mutation[0]):
                        mutated_word = mutation[1] + word[(len(mutation[0])):]
                        return mutated_word
        return word


    def aspirate_mutate(self, word):
        mutable_letters = set(("c", "p", "t"))
        nasal_map = [("ch", "ch"), ("c", "ch"), ("p", "ph"), ("th", "th"), ("t", "th")]
        for mutable_letter in mutable_letters:
            if word.startswith(mutable_letter):            
                for mutation in nasal_map:
                    if word.startswith(mutation[0]):
                        mutated_word = mutation[1] + word[(len(mutation[0])):]
                        return mutated_word
        return word


    def h_prothesise(self, word):
        mutable_letters = set(("a", "e", "i", "o", "w", "y"))
        do_not_mutate_list = set(["a", "i", "o", "w", "y", "yn"])
        if word not in do_not_mutate_list:
            for mutable_letter in mutable_letters:
                if word.startswith(mutable_letter):            
                    mutated_word = "h" + word
                    return mutated_word
        return word


