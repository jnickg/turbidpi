import logging as log
import time

import temp
import cam
import etl
import ipr

def main():
    log.info('Initializing subsystems...')
    log.info('Beginning primary work loop...')
    while True:
        new_readings = etl.Readings()
        temp_c, _ = temp.read_temp()
        frame = cam.read_frame()
        frame_h, frame_w, _ = frame.shape
        img_data = ipr.compress_for_db(frame)
        contrast = ipr.analyze_contrast(frame)

        new_readings.temp_c = temp_c
        new_readings.image = img_data
        new_readings.contrast = contrast
        log.info(f'New readings: {new_readings}')
        time.sleep(15.0)