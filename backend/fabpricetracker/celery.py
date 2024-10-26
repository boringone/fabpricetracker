import os
from django.conf import settings
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fabpricetracker.settings')

app = Celery('fabpricetracker')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

def get_celery_worker_status():
    ERROR_KEY = "ERROR"
    result = {ERROR_KEY: ''}
    try:
        insp = app.control.inspect()
        if not insp.stats():
            return { ERROR_KEY: 'No running Celery workers were found.' }
    except Exception as e:
        from errno import errorcode
        msg = f"Error connecting to the backend: {e}"
        return { ERROR_KEY: msg }
    return result