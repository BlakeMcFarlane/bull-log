from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bull_log.settings')

app = Celery('bull_log')
app.conf.update(timezone='UTC')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

CELERY_RESULT_BACKEND = 'django-db' 

# Celery beat configuration
app.conf.beat_schedule = {
    'every-10-seconds': {
        'task':'base.tasks.scrape_course_data',
        'schedule':30,
    }
}

# Load task modules from all registered Django apps.


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')