#!/usr/bin/env python3
import os
import sys
import json
import codecs

import cherrypy
import logging

from handlers import callback_handler
from assistant.Brain import Brain


class SkillsAPI(object):


    def __init__(self):
        self.brain = Brain()   

 
    @cherrypy.expose
    def index(self):
        msg = "perform_skill/?text=.....\n"
        msg = msg + "expand_intents/?<additional_entities=True|False>i\n"
        return msg


    @cherrypy.expose
    def expand_intents(self, **kwargs):
        additional_entities = kwargs.get('additional_entities', False)
        if additional_entities:
            result = '\n'.join(self.brain.expand_intents(include_additional_entities=True))
        else:
            result = '\n'.join(self.brain.expand_intents(include_additional_entities=False))
        cherrypy.log("expand intents completed")
        return result


    @cherrypy.expose
    @cherrypy.tools.json_out(handler=callback_handler)
    def perform_skill(self, text, **kwargs):

        try:
            if not text:
                raise ValueError("'text' missing")
            latitude = kwargs.get('latitude', 0.0)
            longitude = kwargs.get('longitude', 0.0)
        except ValueError as e:
            return "ERROR: %s" % str(e)

        cherrypy.log("respond to - %s" % text)
        result = {
            'version' : 1
        }

        output = self.brain.handle(text, longitude, latitude)
        result.update({
            'result':output,
            'success':True
        })

        return result


cherrypy.config.update({
    'environment': 'production',
    'log.screen': False,
    'response.stream': True,
    'log.error_file': 'skills-api.log',
})

cherrypy.tree.mount(SkillsAPI(), '/')
application = cherrypy.tree

