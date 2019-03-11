
from assistant.Brain import Brain
from celery import Celery

app = Celery('skills_assistant_tasks', broker='pyamqp://guest@localhost//')

@app.task
def initialize_recordings_database_task(self, brain):
    brain.initialize_recordings_database()

