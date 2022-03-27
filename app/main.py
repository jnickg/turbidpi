# system imports
import os
import sys
import logging as log
import signal
import argparse
import datetime
import time
# external imports
from readchar import readchar
import pandas as pd
# local imports
from fun import CONSOLE_BANNER
from temp import read_temp
from cam import read_frame
import etl

LOGGING_FILE = 'mrm.log'
LOGGING_FORMAT = '%(asctime)s [ %(levelname)s ] %(message)s'
LOGGING_DATE_FORMAT = '%Y/%m/%d %H:%M:%S'
LOGGING_LEVEL = log.DEBUG

def deinit_systems():
    pass

def exit_program(code:int = 0):
    log.info('Exiting...')
    deinit_systems()
    sys.exit(code)

def sigint_handler(signum, frame):
    print('', end='\r', flush=True)
    log.info('SIGINT HANDLER HIT')
    confirm_msg = 'Do you really want to exit? (y/n): '
    print(confirm_msg, end='', flush=True)
    res = readchar()
    print('', end='\r', flush=True)
    print(' ' * len(confirm_msg), end='', flush=True) # clears confirmation message
    print('     ', end='\r', flush=True)
    if res == 'y':
        exit_program(1)


def main():
    parser = argparse.ArgumentParser()
    # TODO add arguments :-)
    args = parser.parse_args()

    df = pd.DataFrame(columns = etl.DATAFRAME_COLUMNS)
    log.info('Created empty DataFrame. Beginning primary work loop...')

    while True:
        ct = datetime.datetime.now()
        temp_c, _ = read_temp()
        frame = read_frame()
        frame_w, frame_h, _ = frame.shape
        log.debug(f'{ct} READINGS - temp:{temp_c} frame_w:{frame_w} frame_h:{frame_h}')
        pd.concat([df, pd.DataFrame({
            etl.TIMESTAMP_COL: [ct],
            etl.TEMP_C_COL: [temp_c],
            etl.FRAME_W_COL: [frame_w],
            etl.FRAME_H_COL: [frame_h],
        })])
        time.sleep(15.0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)
    log.basicConfig(stream = sys.stdout,
                    format = LOGGING_FORMAT,
                    datefmt = LOGGING_DATE_FORMAT,
                    level = LOGGING_LEVEL)
    os.system('clear')
    print(CONSOLE_BANNER)
    log.info('Starting monitor...')
    try:
        main()
    except Exception as e:
        log.error(f'Something went wrong: {e}')
        log.exception(e)
    exit_program(0)