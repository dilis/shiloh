from pipeline import analyze, app, ingest

import dotenv
import glob
import os
import signal
import subprocess
import time

def call_analyze():
    inspect = app.control.inspect()
    active_workers = inspect.active()
    if active_workers:
        for worker, tasks in active_workers.items():
            # print(f'Worker: {worker}, type: {type(worker)} tasks: {tasks}')
            if not tasks:
                # call the analyze task of this worker
                analyze.delay()

        time.sleep(1)
        active_workers = inspect.active()
        print(f'Active workers: {active_workers.values()}')
        print(all([len(tasks) == 0 for tasks in active_workers.values()]))
        while not all([len(tasks) == 0 for tasks in active_workers.values()]):
            time.sleep(1)
            active_workers = inspect.active()
            print(f'Active workers: {active_workers.values()}')
            print(all([len(tasks) == 0 for tasks in active_workers.values()]))

celery_workers = []
def start_workers(worker_count: int):
    for i in range(worker_count):
        p = subprocess.Popen(['celery', '-A', 'pipeline', 'worker', '-l', 'info', '-n', f'worker.{i}', '--concurrency', '1'])
        celery_workers.append(p)

def stop_workers():
    for p in celery_workers:
        p.send_signal(signal.SIGTERM)
        # p.wait()

def main():
    dotenv.load_dotenv()
    worker_count = int(os.getenv('CELERY_WORKER_COUNT', 1))
    start_workers(worker_count)
    # give workers time to initialize
    time.sleep(5)

    try:
        while True:
            files = glob.glob('data/*.json')
            # files = []
            if files:
                fname = files[0]
                print(f'Processing {fname}')
                ingest(fname)
                call_analyze()
                # os.rename(fname, f'{fname}.processed')
                break
            else:
                time.sleep(1)
    finally:
        stop_workers()

if __name__ == '__main__':
    main()