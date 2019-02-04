#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import feedparser

from Skill import Skill
from padatious import IntentContainer

class newyddion_skill(Skill):

    def __init__(self, root_dir, name, nlp):
        super(newyddion_skill, self).__init__(root_dir, name, nlp)


    def handle(self, intent_parser_result):

        result = "Dyma bennawdau gwefan newyddion Golwg 360\n"

        rss_url = 'https://golwg360.cymru/%s/ffrwd'
        subject = intent_parser_result.matches.get('subject')

        if subject is None:
           rss_url = rss_url % 'newyddion'
        else:
           rss_url = rss_url % subject

        rss = feedparser.parse(rss_url)
        for entry in rss.get("entries")[:5]:
            result = result + entry.get("title") + '\n'
            result = result + entry.get('description') + '\n\n'

        return result
        
