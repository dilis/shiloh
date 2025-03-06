from celery import Celery

import time

app = Celery('pipeline', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@app.task
def ingest(fname: str):
    print(f'Ingesting {fname}')
    time.sleep(5)
    return f'{fname}.ingested'

@app.task
def analyze():
    print('Analyzing data')
    time.sleep(5)
    return 'analysis.json'