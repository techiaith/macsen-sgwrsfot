#!/usr/bin/env python3
import os
import sys
import json
import codecs
import cherrypy
import logging

from assistant.Brain import Brain
from assistant.RecordingsDatabase import RecordingsDatabase


class SkillsAPI(object):


    def __init__(self):
        self.brain = Brain(online=True)
        self.recordings_database = RecordingsDatabase()


    @cherrypy.expose
    def index(self):
        msg = "perform_skill/?text=....."
        msg = msg + "<br/>"
        msg = msg + "get_all_sentences/?<additional_entities=True|False>"
        msg = msg + "<br/>"
        msg = msg + "get_all_skills_intents_sentences/"
        msg = msg + "<br/>"
        msg = msg + "get_unrecorded_sentence/?uid=....."
                
        return msg


    @cherrypy.expose
    @cherrypy.tools.json_out()
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
    @cherrypy.tools.json_out()
    def get_all_sentences(self, **kwargs):

        cherrypy.log("get_all_sentences...")

        sentences = self.recordings_database.select_sentences() 
        result = {
                'version': 1
        }
        result.update({
            'result':sentences,
            'success':True
        })
        return result


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_all_skills_intents_sentences(self, **kwargs):
        skills_intents_sentences = self.recordings_database.select_skills_intents_sentences()
        result = {
                'version': 1
        }
        result.update({
            'result':skills_intents_sentences,
            'success':True
            })
        return result


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def perform_skill(self, text, **kwargs):
        try:
            if not text:
                raise ValueError("'text' missing")
            latitude = float(kwargs.get('latitude', 0.0))
            longitude = float(kwargs.get('longitude', 0.0))
        except ValueError as e:
            return "ERROR: %s" % str(e)

        cherrypy.log("respond to - %s, latitude: %s, longitude: %s " % (text, latitude, longitude))

        result = {
            'version' : 1
        }

        intent_name, output = self.brain.handle(text, latitude, longitude)

        success=True
        if output is None:
            success=False

        result.update({
            'intent':intent_name,
            'result':output,
            'success':success
        })

        cherrypy.log(json.dumps(result,indent=1))

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
    'log.error_file': '/var/log/skills-server/cherrypy.error.log',
})

cherrypy.tree.mount(SkillsAPI(), '/')
application = cherrypy.tree

