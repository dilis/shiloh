from pipeline import ingest

import glob
import os
import time

def main():
    while True:
        files = glob.glob('data/*.json')
        if files:
            fname = files[0]
            print(f'Processing {fname}')
            ingest(fname)
            
            os.rename(fname, f'{fname}.processed')
        else:
            time.sleep(1)

if __name__ == '__main__':
    main()