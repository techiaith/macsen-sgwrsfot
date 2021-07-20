# -*- coding: utf-8 -*-
import os
import feedparser

from Skill import Skill

from padatious import IntentContainer

from html.parser import HTMLParser


class newyddion_skill(Skill):


    def __init__(self, root_dir, name, nlp, active):
        super(newyddion_skill, self).__init__(root_dir, name, nlp, active)
        self.html_parser = HTMLParser()


    def handle(self, intent_parser_result, latitude, longitude):

        skill_response = []
        context = intent_parser_result.matches

        rss_url = 'https://golwg360.cymru/%s/ffrwd'
        title = ''

        if 'subject' in context.keys():
            subject = context["subject"]
            subject = subject.replace('?', '')
            rss_url = rss_url % self.handle_subject_website_mappings(subject)
            title = "Dyma benawdau %s gwefan newyddion Golwg 360" % subject
        elif 'country' in context.keys():
            country = context["country"]
            country = country.replace('?', '')
            rss_url = rss_url % country
            title = "Dyma benawdau %s gwefan newyddion Golwg 360" % country.title()
        else:
            rss_url = rss_url % 'newyddion'
            title = "Dyma benawdau gwefan newyddion Golwg 360"

        title = title + "."

        skill_response.append({
            'title': title,
            'description': '',
            'url': ''})

        rss = feedparser.parse(rss_url)
        for entry in rss.get("entries")[:5]:
            skill_response.append({
                'title': self.html_parser.unescape(entry.get("title") + "."),
                'description': self.html_parser.unescape(entry.get('description') + "."),
                'url': entry.get('link')
            })

        return skill_response


    def handle_subject_website_mappings(self, subject):
        if subject in ['rygbi', 'criced']:
            return "chwaraeon/%s" % subject
        if subject in ['pêl droed',"pel droed", "pêl-droed"]:
            return "chwaraeon/pel-droed"
        if subject=="busnes":
            return 'arian-a-busnes'
        return subject


