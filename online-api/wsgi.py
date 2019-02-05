#!/usr/bin/env python3
import os
import sys
import json
import codecs

import cherrypy
import logging

from assistant.Brain import Brain


class SkillsAPI(object):

    def __init__(self):
        self.brain = Brain()   

 
    @cherrypy.expose
    def index(self):
        return "perform_skill/?text=....."


    @cherrypy.expose
    def expand_intents(self, **kwargs):
        cherrypy.log("performing expand intents")
        result = '\n'.join(self.brain.expand_intents())
        cherrypy.log("expand intents completed")
        return result


    @cherrypy.expose
    def perform_skill(self, text, **kwargs):
        cherrypy.log("performing skill for text:  '%s'" % text)
        try:
            if not text:
                raise ValueError("'text' missing")
        except ValueError as e:
            return "ERROR: %s" % str(e)

        result = self.brain.handle(text)

        cherrypy.log('skills result %s ' % result)
        return result


cherrypy.config.update({
    'environment': 'production',
    'log.screen': False,
    'response.stream': True,
    'log.error_file': 'skills-api.log',
})

cherrypy.tree.mount(SkillsAPI(), '/')
application = cherrypy.tree

