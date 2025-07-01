import time

from celery import shared_task


@shared_task
def mine():
    time.sleep(5)