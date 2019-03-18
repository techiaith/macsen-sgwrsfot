from celery import Celery
from RecordingsDatabase import RecordingsDatabase
from nlp.cy.cysill import CysillArleinAPI

app = Celery('skills_assistant_tasks', broker='pyamqp://guest@localhost//')

@app.task
def initialize_recordings_database_task(all_skill_sentences):

    mysql_db = RecordingsDatabase()

    for skill in all_skill_sentences:
        for intent in all_skill_sentences[skill]:
            sanitized_sentences = [] 
            for sentence in all_skill_sentences[skill][intent]:
              
                if len(s) ==0;
                    continue

                if '{' in sentence and '}' in sentence:
                    continue

                sanitized_sentences.append(sentence)

            mysql_db.add_sentences(skill, intent, sanitized_sentences) 


