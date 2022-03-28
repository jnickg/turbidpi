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
import const
import dvc

LOGGING_FILE = 'mrm.log'
LOGGING_FORMAT = '%(asctime)s - %(filename)10s:%(funcName)20s [ %(levelname)10s ] %(message)s'
LOGGING_DATE_FORMAT = '%Y/%m/%d %H:%M:%S'
LOGGING_LEVEL = log.DEBUG

def deinit_systems():
    pass

def exit_program(code:int = 0):
    log.info(f'Exiting (code = {code})...')
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
    parser.add_argument('--config', '-c', help='Launch %(prog)s as one of \''+const.CONFIG_DEVICE+'\' (device), \''+const.CONFIG_REST+'\' (REST backend), or \''+const.CONFIG_WEB+'\' (frontend server)', type=str, default=const.CONFIG_DEVICE, choices=[const.CONFIG_DEVICE, const.CONFIG_REST, const.CONFIG_WEB])
    args = parser.parse_args()

    log.info(f'Launching with system configuration: {args.config}...')
    if args.config == const.CONFIG_DEVICE:
        dvc.main()
    elif args.config == const.CONFIG_REST:
        pass
    elif args.config == const.CONFIG_WEB:
        pass
    else:
        # Shouldn't be hit with above "choices" on argument, but it's more maintainble to leave
        # this here, just in case.
        log.error(f'Invalid value for --config argument: {args.config}.')
        parser.print_help()
        exit_program(-1)

    # We got to the end without an error
    exit_program(0)


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