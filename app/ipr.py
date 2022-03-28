import os
import io
import logging as log
import time

import cv2 as cv
import numpy as np

from timer import Timer

DOWNSAMPLE_W = 480
DOWNSAMPLE_H = 270

def analyze_contrast(frame:np.ndarray) -> float:
    with Timer('analyze_contrast'):
        frame_grey = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        contrast = frame_grey.std()
        return contrast

def compress_for_db(frame:np.ndarray) -> bytearray:
    with Timer('compress_for_db'):
        pre_bytes = frame.nbytes
        small_frame = cv.resize(frame, (DOWNSAMPLE_H, DOWNSAMPLE_W), interpolation = cv.INTER_LANCZOS4)
        _, jpeg_frame = cv.imencode('.jpg', small_frame, [cv.IMWRITE_JPEG_QUALITY, 75])
        buffer = io.BytesIO(jpeg_frame)
        out_bytes = buffer.read()
        post_bytes = len(out_bytes)
        log.debug(f'Compressed {pre_bytes}b → {post_bytes}b')
        return out_bytes
