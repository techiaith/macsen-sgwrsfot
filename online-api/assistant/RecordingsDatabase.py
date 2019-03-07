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


    def initialize(self, sentences):
        print ("RecordingDatabase init")
        self.create_database_if_not_exists()
        self.create_recorded_sentences_table_if_not_exists()
        self.create_sentences_tables(sentences)


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


    def create_sentences_tables(self, sentences):
        self.execute_sql("""
              DROP TABLE IF EXISTS Sentences
              """)

        self.execute_sql("""
              CREATE TABLE Sentences 
              (
                  guid VARCHAR(100) NOT NULL, 
                  sentence VARCHAR(10000), 
                  PRIMARY KEY (guid)
              )""")

        db_data = []
        for s in sentences:
           guid=self.hash(s)
           if (guid, s) in db_data:
               continue
           db_data.append((guid, s)) 
           
        sql_insert = "INSERT INTO Sentences (guid, sentence) VALUES (%s, %s)"
        self.execute_many_sql(sql_insert, db_data)

    def select_sentences(self):
        result = []
        cnx = pymysql.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_NAME)
        cursor = cnx.cursor()
        cursor.execute("""
            SELECT sentence FROM Sentences
        """)

        result=cursor.fetchall()
        cnx.close()
        return result
         

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

