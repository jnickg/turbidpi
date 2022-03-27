# system imports
import os
import sys
import logging as log
import signal
import argparse
import datetime
import time
from dataclasses import asdict
# external imports
from readchar import readchar
import pandas as pd
# local imports
from fun import CONSOLE_BANNER
from temp import read_temp
from cam import read_frame, compress_for_db
import etl

LOGGING_FILE = 'mrm.log'
LOGGING_FORMAT = '%(asctime)s - %(filename)10s:%(funcName)20s [ %(levelname)10s ] %(message)s'
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
    confirm_msg = 'Do you really want to exit? (y/n): '
    log.info(f'SIGINT HANDLER - GETTING USER INPUT WITH PROMPT \'{confirm_msg}\'')
    print(confirm_msg, end='', flush=True)
    res = readchar()
    print('', end='\r', flush=True)
    print(' ' * len(confirm_msg), end='', flush=True) # clears confirmation message
    print('     ', end='\r', flush=True)
    log.info(f'USER PRESSED \'{res}\'')
    if res == 'y':
        exit_program(1)


def main():
    parser = argparse.ArgumentParser()
    # TODO add arguments :-)
    args = parser.parse_args()

    log.info('Beginning primary work loop...')
    while True:
        new_readings = etl.Readings()
        temp_c, _ = read_temp()
        frame = read_frame()
        frame_h, frame_w, _ = frame.shape
        img_data = compress_for_db(frame)

        new_readings.temp_c = temp_c
        new_readings.image = img_data
        log.info(f'New readings: {new_readings}')
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