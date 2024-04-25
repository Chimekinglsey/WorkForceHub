# celery.py

from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab
import os
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'workforcehub.settings')

app = Celery('workforcehub')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'reset_monthly_created_employees': {
        'task': 'organizations.tasks.reset_monthly_created_employees',
        'schedule': crontab(day_of_month='1', hour=0, minute=0),  # Run at midnight of every first day of the month
    },
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
