from celery import Celery
from RecordingsDatabase import RecordingsDatabase
from nlp.cy.cysill import CysillArleinAPI

app = Celery('skills_assistant_tasks', broker='pyamqp://guest@localhost//')

@app.task
def initialize_recordings_database_task(all_sentences, ignore_dictionary_file_path):
    proofed_sentences = []

    mysql_db = RecordingsDatabase()
    cysill_api = CysillArleinAPI()
    cysill_api.open_ignore_words(ignore_dictionary_file_path)

    for s in all_sentences:
        if len(s) == 0:
            continue

        if '{' in s and '}' in s:
            continue

        errors = cysill_api.get_errors(s)
        if (len(errors)) == 0:
           proofed_sentences.append(s)
        else:
           print ("Error: %s" % s)

    mysql_db.initialize(proofed_sentences)

