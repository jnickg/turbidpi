import os
import io
import logging as log

import cv2 as cv
import numpy as np

import picamera

vid = cv.VideoCapture(0)
vid.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
vid.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)

DOWNSAMPLE_W = 480
DOWNSAMPLE_H = 270

def read_frame() -> np.ndarray:
    cap, frame = vid.read()
    return frame

def compress_for_db(frame:np.ndarray) -> bytearray:
    pre_bytes = frame.nbytes
    small_frame = cv.resize(frame, (DOWNSAMPLE_H, DOWNSAMPLE_W), interpolation = cv.INTER_LANCZOS4)
    _, jpeg_frame = cv.imencode('.jpg', small_frame, [cv.IMWRITE_JPEG_QUALITY, 75])
    buffer = io.BytesIO(jpeg_frame)
    out_bytes = buffer.read()
    post_bytes = len(out_bytes)
    log.debug(f'Compressed {pre_bytes}b → {post_bytes}b')
    return out_bytes
