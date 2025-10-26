import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sendEverywhere.settings')

app = Celery('sendEverywhere')

# Load Celery settings from Django settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks from installed apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Optional scheduled task
app.conf.beat_schedule = {
    'delete_expired_files_task': {
        'task': 'base.task.delete_expired_files',
        'schedule': 300.0,  # 1 minutes
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
