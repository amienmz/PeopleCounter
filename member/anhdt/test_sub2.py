__author__ = 'anhdt'
import numpy as np
import cv2

cap = cv2.VideoCapture(1)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(4,4))
fgbg = cv2.BackgroundSubtractorMOG2()
r,f = cap.read()
avg1 = np.float32(f)
while(1):
    ret, frame = cap.read()
    framex = frame
    # frame = cv2.medianBlur(frame,7)
    # cv2.accumulateWeighted(frame,avg1,0.01)
    fgmask = fgbg.apply(frame)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    # contours, hierarchy = cv2.findContours(fgmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # # print contours
    # intruders = []
    # for x in contours:
    #     area = cv2.contourArea(x)
    #     if (area > 5000 and area < 90000):
    #         intruders.append(x)
    # cv2.drawContours(fgmask, intruders, -1, (255,255,255), -1)
    display = cv2.bitwise_and(framex,framex,None,fgmask)

    cv2.imshow("frame",frame)
    cv2.imshow('sub',fgmask)
    cv2.imshow('res',display)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()