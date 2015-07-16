from __future__ import absolute_import

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learn_django.settings.dev')

from django.conf import settings

app = Celery('proj', broker='amqp://guest@localhost:5672//', include=['blog.tasks'])  # default broker

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# Optional configuration, see the application user guide.
"""app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)"""

if __name__ == '__main__':
    app.start()    