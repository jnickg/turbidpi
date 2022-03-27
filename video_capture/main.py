import picamera
import os
import cv2 as cv

vid = cv.VideoCapture(0)
vid.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
vid.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
cap, frame = vid.read()
cv.imwrite('test.png', frame)
