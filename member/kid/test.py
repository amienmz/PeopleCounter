import time

__author__ = 'pc'

import cv2

cap = cv2.VideoCapture(0)
cap.set(3,352)
cap.set(4,288)
# print cap.set(5,25)
while 1:
    first = time.time()
    ret,frame = cap.read()
    frame = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
    cv2.imshow('huy',frame)

    print str(time.time()-first)

    # cv2.waitKey(100)

