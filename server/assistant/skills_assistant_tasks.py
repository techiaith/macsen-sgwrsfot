from celery import Celery
from RecordingsDatabase import RecordingsDatabase

app = Celery('skills_assistant_tasks', broker='pyamqp://guest@localhost//')

@app.task
def initialize_skills_database_task(all_skills):

    mysql_db = RecordingsDatabase()
    
    for skill_name, active in all_skills:
        mysql_db.add_skill(skill_name, active)


@app.task
def initialize_recordings_database_task(all_skill_sentences):

    mysql_db = RecordingsDatabase()

    for skill in all_skill_sentences:
        for intent in all_skill_sentences[skill]:
            sanitized_sentences = [] 
            for sentence in all_skill_sentences[skill][intent]:
              
                if len(sentence)==0:
                    continue

                if '{' in sentence and '}' in sentence:
                    continue

                sanitized_sentences.append(sentence)

            mysql_db.add_sentences(skill, intent, sanitized_sentences) 

