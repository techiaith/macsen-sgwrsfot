#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import pymysql.cursors

DB_HOST = "mysql"
DB_USER = "root"
DB_PASSWORD = "Mac53n"
DB_NAME = "Macsen"


class RecordingsDatabase(object):


    def __init__(self):
        pass


    def initialize(self):
        self.create_database_if_not_exists()
        self.create_recorded_sentences_table_if_not_exists()
        self.create_sentences_table()
        self.create_active_skills_table()


    def create_database_if_not_exists(self):
        cnx = pymysql.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        cursor = cnx.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS %s" % DB_NAME)
        cnx.close() 


    def create_recorded_sentences_table_if_not_exists(self):
        self.execute_sql("""
              CREATE TABLE IF NOT EXISTS RecordedSentences 
              (
                 uid VARCHAR(100) NOT NULL, 
                 guid VARCHAR(100) NOT NULL,
                 PRIMARY KEY (uid, guid)
              )""")


    def create_sentences_table(self):
        self.execute_sql("""
              DROP TABLE IF EXISTS Sentences
              """)

        self.execute_sql("""
              CREATE TABLE Sentences 
              (
                  guid VARCHAR(100) NOT NULL, 
                  skill_name VARCHAR(50) NOT NULL,
                  intent_name VARCHAR(50) NOT NULL,
                  sentence VARCHAR(10000), 
                  PRIMARY KEY (guid)
              )""")


    def create_active_skills_table(self):
        self.execute_sql("""
             DROP TABLE IF EXISTS Skills
             """)

        self.execute_sql("""
             CREATE TABLE Skills
             (
                 skill_name VARCHAR(50) NOT NULL,
                 active BOOLEAN NOT NULL,
                 PRIMARY KEY (skill_name)
             )""")            


    def add_skill(self, skill_name, active): 
        db_data = []
        db_data.append((skill_name, active))
        sql_insert = "INSERT INTO Skills (skill_name, active) VALUES (%s, %s)"
        self.execute_many_sql(sql_insert, db_data)


    def add_sentences(self, skill_name, intent_name, sentences):
        db_data = []
        for s in sentences:
           guid=self.hash(s)
           if (guid, s) in db_data:
               continue
           db_data.append((guid, skill_name, intent_name, s)) 
           
        sql_insert = "INSERT INTO Sentences (guid, skill_name, intent_name, sentence) VALUES (%s, %s, %s, %s)"
        self.execute_many_sql(sql_insert, db_data)


    def select_sentences(self):
        result = []
        cnx = pymysql.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_NAME)
        cursor = cnx.cursor()
        cursor.execute("""
            SELECT sentence FROM Sentences ORDER BY skill_name, intent_name, sentence
        """)

        db_result=cursor.fetchall()
        result=[]
        for r in db_result:
            result.append(r)
 
        cnx.close()
        return result


    def select_skills_intents_sentences(self):
        skills={}
        
        cnx = pymysql.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_NAME)
        cursor = cnx.cursor()
        cursor.execute("""
            SELECT s.skill_name, s.intent_name, s.sentence 
            FROM Sentences as s, Skills as k 
            WHERE s.skill_name = k.skill_name AND k.active=1
            ORDER BY s.skill_name, s.intent_name, s.sentence
        """)

        db_result=cursor.fetchall()
        for skill_name, intent_name, sentence in db_result:
            if skill_name not in skills:
                intents={}
                sentences=[]
                intents[intent_name]=sentences
                skills[skill_name]=intents
            
            if intent_name not in skills[skill_name]:
                sentences=[]
                skills[skill_name][intent_name]=sentences
 
            skills[skill_name][intent_name].append(sentence)

        cnx.close()
        return skills

    
    def select_skills_sentences(self):
        result = []


    def select_random_unrecorded_sentence(self, uid):
        unrecorded_sentence = ''
        cnx = pymysql.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_NAME)
        cursor = cnx.cursor()
        result = cursor.execute("""
            SELECT s.sentence FROM Sentences s
            WHERE s.guid NOT IN 
            (
               SELECT rs.guid FROM RecordedSentences rs
               WHERE rs.uid=%s 
            ) ORDER BY RAND() LIMIT 1
        """, (uid))

        if result > 0:
            unrecorded_sentence = cursor.fetchone()

        cnx.close()
        return unrecorded_sentence


    def sentence_is_recorded(self, uid, sentence):
        db_data = []
        sentence_hash = self.hash(sentence)
        db_data.append((uid, sentence_hash)) 
        sql_insert = "INSERT INTO RecordedSentences (uid, guid) VALUES (%s, %s)"
        self.execute_many_sql(sql_insert, db_data)
        return sentence_hash


    def execute_sql(self, sql):
        cnx = pymysql.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_NAME)
        cursor = cnx.cursor()
        cursor.execute(sql)
        cnx.close()


    def execute_many_sql(self, sql, db_data):
        cnx = pymysql.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_NAME)
        cursor = cnx.cursor()
        cursor.executemany(sql, db_data)
        cnx.commit()
        cnx.close()
       

    def hash(self, sentence):
        return hashlib.md5(sentence.encode('utf-8')).hexdigest()


if __name__ == "__main__":
    db=RecordingsDatabase()
    print (db.select_skills_intents_sentences())
