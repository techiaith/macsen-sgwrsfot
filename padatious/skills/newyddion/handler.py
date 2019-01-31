#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pprint
import feedparser

from padatious import IntentContainer

class newyddion_handler:

    def handle(self, intent_parser_result):

        result = "Dyma bennawdau gwefan newyddion Golwg 360\n"

        rss_url = 'https://golwg360.cymru/newyddion<SUBJECT>ffrwd'
        subject = intent_parser_result.matches.get('subject')

        if subject is None:
           rss_url = rss_url.replace("<SUBJECT>",'/')
        else:
           rss_url = rss_url.replace('<SUBJECT>','/%s/' % subject)

        rss = feedparser.parse(rss_url)
        for entry in rss.get("entries")[:5]:
            result = result + entry.get("title") + '\n'
            result = result + entry.get('description') + '\n\n'

        return result
        
