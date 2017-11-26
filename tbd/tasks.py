from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from kombu import Queue
import time
import sys
import json
from kombu.common import Broadcast
from subprocess import Popen, PIPE
from kombu import Exchange, Queue
from celery.signals import task_postrun, worker_shutdown, task_prerun, celeryd_after_setup, task_postrun
from celery import signals
from celery.worker.control import control_command
from billiard import current_process
from requests import Session

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = Celery('ap_domain_worker')
# app.config_from_object('tbd.celeryconfig')
app.conf.update(
    broker_url = 'amqp://admin:admin*123@192.168.1.245/',
    result_backend = 'rpc://',
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    result_expires=1*60,
    task_queues=(Broadcast('broadcast_tasks'), Queue('celery')),
    task_routes={
        'tbd.tasks.upgrade': {
            'queue': 'broadcast_tasks',
            'exchange': 'broadcast_tasks'
        }
    }
)

@celeryd_after_setup.connect
def capture_worker_name(sender, instance, **kwargs):
    os.environ["CELERY_WORKER_NAME"] = sender

@control_command()
def reload_worker(state, msg='Got shutdown from remote', **kwargs):
    print(msg)
    controller = state.app.WorkController(state.app)
    print(controller)
    # print(controller.state)
    controller.terminate()

@task_prerun.connect
def init_task(sender=None, task=None, task_id=None, **kwargs):
    print('worker {0!r} task {1!s} is running with request: {2}'.format(task.app.Worker, task_id, task.request))

@task_postrun.connect
def done_task(sender=None, task=None, task_id=None, retval=None, **kwargs):
    print('sender {0!r} task {1!s} is done with result: {2}'.format(sender.name, task_id, retval))
    if sender.name == "tbd.tasks.query_issue_frequency":
        resp = Session().post('http://127.0.0.1:8001/auto/task_result', {
            'task_id': task_id,
            'task_result': json.dumps(retval),
        })

@app.task(bind=True)
def query_issue_frequency(self, issue_id):
    for i in range(2):
        print("study do job for {}".format(i))
        time.sleep(1)
        # raise ValueError("Test exception")
    result = {
        'builds': {
            'builds1': {
                'dut1': ['jira1', 'jira2',],
                'dut3': ['jira3', 'jira4',],
                'dut4': ['jira5', 'jira6',],
            },
            'builds2': {
                'dut2': ['jira7', 'jira8',],
                'dut3': ['jira9',],
                'dut4': ['jira10', 'jira11', 'jira12',],
            },
        }
    }
    return result

@app.task(bind=True, ignore_result=False)
def upgrade(self):
    self.app.control.broadcast('shutdown', destination=[os.environ["CELERY_WORKER_NAME"]])
    proc = Popen("svn update", stdout=PIPE, stderr=PIPE)
    output, error = proc.communicate()
    return {'stdout': bytes.decode(output), 'stderr': bytes.decode(error), 'code': proc.returncode }