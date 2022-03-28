import time
import logging as log

class Timer:
    def __init__(self, name:str=''):
        self.name = name

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.elapsed_s = self.end - self.start
        self.elapsed_ms = self.elapsed_s * 1000
        self.report_runtime()

    def report_runtime(self):
        log.debug(f'Completed operation \'{self.name}\' in {self.elapsed_ms:0.5f}ms')