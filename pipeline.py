from celery import Celery
from os import getenv

import dotenv
import time

dotenv.load_dotenv()

broker = getenv('CELERY_BROKER')
backend = getenv('CELERY_RESULT_BACKEND')
app = Celery('pipeline', broker=broker, backend=backend)

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