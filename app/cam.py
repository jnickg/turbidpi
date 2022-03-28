import os
import io
import logging as log
import time
import threading
import subprocess

import cv2 as cv
import numpy as np

import picamera

from timer import Timer


vid_settings_lock = threading.RLock()
vid = None




def _set_property_v4l2(property, value):
    global vid_settings_lock
    with vid_settings_lock:
        try:
            subprocess.call(['sudo', 'v4l2-ctl', '-c', f'{property}={value}'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
            log.info(f'Set camera property: {property} to value: {value}')
        except Exception as e:
            log.exception(e)
            log.error(f'Failed to set camera property: {property} to value: {value}')

def _get_property_v4l2(property):
    result = None
    global vid_settings_lock
    with vid_settings_lock:
        try:
            result = subprocess.check_output(['v4l2-ctl', '-C', f'{property}'])
            result = result.decode('utf-8').split()[1]
        except Exception as e:
            log.exception(e)
            log.error(f'Failed to get value of camera property: {property}')
    return result

class CameraSettings:
    pass # TODO make properties for each setting we like



def init_camera(reinit:bool=False):
    global vid
    global vid_settings_lock
    with vid_settings_lock:
        if reinit or vid is None:
            vid = cv.VideoCapture(0)
            vid.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
            vid.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)

def read_frame() -> np.ndarray:
    init_camera()
    with Timer('read_frame'):
        _, frame = vid.read()
    return frame