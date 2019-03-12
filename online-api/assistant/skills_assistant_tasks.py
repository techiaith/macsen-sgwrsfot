from celery import Celery
from RecordingsDatabase import RecordingsDatabase
from nlp.cy.cysill import CysillArleinAPI

app = Celery('skills_assistant_tasks', broker='pyamqp://guest@localhost//')

@app.task
def initialize_recordings_database_task(all_sentences, ignore_dictionary_file_path):

    mysql_db = RecordingsDatabase()

    cysill_api = CysillArleinAPI()
    cysill_api.open_ignore_words(ignore_dictionary_file_path)

    for skill_name, skill_sentences in all_sentences.items():
        print (skill_name)
        print (skill_sentences) 
        proofed_sentences = []

        for s in skill_sentences:
            if len(s) == 0:
                continue

            if '{' in s and '}' in s:
                continue

            try:
                errors = cysill_api.get_errors(s)
                if (len(errors)) == 0:
                    print (s)
                    proofed_sentences.append(s)
                else:
                    print ("Error: %s" % s)
            except:
                print ("Exception...")

        mysql_db.add_skill_sentences(skill_name, proofed_sentences)


