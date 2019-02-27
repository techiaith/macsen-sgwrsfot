#!/usr/bin/env python3
import os
import sys
import json
import codecs

import cherrypy
import logging

from handlers import callback_handler
from assistant.Brain import Brain
from assistant.RecordingsDatabase import RecordingsDatabase

class SkillsAPI(object):


    def __init__(self):
        self.brain = Brain()
        self.recordings_database = RecordingsDatabase()

 
    @cherrypy.expose
    def index(self):
        msg = "perform_skill/?text=.....\n"
        msg = msg + "get_all_sentences/?<additional_entities=True|False>i\n"
        msg = msg + "get_unrecorded_sentence/?uid=.....\n"
        return msg


    @cherrypy.expose
    @cherrypy.tools.json_out(handler=callback_handler)
    def get_unrecorded_sentence(self, uid, **kwargs):
        try:
            if not uid:
                raise ValueError("'uid' missing")
        except ValueError as e:
            return "ERROR: %s" % str(e)

        sentence = self.brain.get_unrecorded_sentence(uid)
        result = {
                'version' : 1
        }
        result.update({
            'result':sentence,
            'success':True
        })
        return result


    @cherrypy.expose
    def get_all_sentences(self, **kwargs):
        additional_entities = kwargs.get('additional_entities', False)
        if additional_entities:
            result = '\n'.join(self.brain.expand_intents(include_additional_entities=True))
        else:
            result = '\n'.join(self.brain.expand_intents(include_additional_entities=False))
        return result


    @cherrypy.expose
    @cherrypy.tools.json_out(handler=callback_handler)
    def perform_skill(self, text, **kwargs):
        try:
            if not text:
                raise ValueError("'text' missing")
            latitude = float(kwargs.get('latitude', 0.0))
            longitude = float(kwargs.get('longitude', 0.0))
        except ValueError as e:
            return "ERROR: %s" % str(e)

        cherrypy.log("respond to - %s" % text)
        result = {
            'version' : 1
        }

        intent_name, output = self.brain.handle(text, longitude, latitude)
        result.update({
            'intent':intent_name,
            'result':output,
            'success':True
        })

        return result


    @cherrypy.expose
    def upload_recorded_sentence(self, uid, sentence, soundfile, **kwargs):
        upload_dir_path =  os.path.join("/recordings", uid)
        if not os.path.exists(upload_dir_path):
            os.makedirs(upload_dir_path)

        hashed_file_name = self.recordings_database.sentence_is_recorded(uid, sentence) 

        # create two files, wav and txt
        sentence_txt_file_path = os.path.join(upload_dir_path, hashed_file_name + ".txt")
        with open(sentence_txt_file_path, 'w', encoding='utf-8') as txtfile:
            txtfile.write(sentence)

        sentence_wav_file_path = os.path.join(upload_dir_path, hashed_file_name + '.wav')
        with open(sentence_wav_file_path, 'wb') as wavfile:
            while True:
                data = soundfile.file.read(8192)
                if not data:
                    break;
                wavfile.write(data)


cherrypy.config.update({
    'environment': 'production',
    'log.screen': False,
    'response.stream': True,
    'log.error_file': 'skills-api.log',
})

cherrypy.tree.mount(SkillsAPI(), '/')
application = cherrypy.tree

