from celery import Celery
from RecordingsDatabase import RecordingsDatabase
from nlp.cy.cysill import CysillArleinAPI

app = Celery('skills_assistant_tasks', broker='pyamqp://guest@localhost//')

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

@app.task
def initialize_recordings_database_task(all_sentences):
    logger.info("initialize_recordings_database_task.....")
    proofed_sentences = []

    mysql_db = RecordingsDatabase()
    cysill_api = CysillArleinAPI()

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


