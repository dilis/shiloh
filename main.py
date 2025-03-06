from pipeline import analyze, app, ingest

import glob
import os
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


def main():
    # inspector = app.control.inspect()
    # active_workers = inspector.active()
    # print(f'Active workers: {active_workers}')
    while True:
        files = glob.glob('data/*.json')
        if files:
            fname = files[0]
            print(f'Processing {fname}')
            ingest(fname)
            call_analyze()
            # os.rename(fname, f'{fname}.processed')
        else:
            time.sleep(1)

if __name__ == '__main__':
    main()