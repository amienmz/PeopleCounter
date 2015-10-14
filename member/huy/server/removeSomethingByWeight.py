__author__ = 'huybu'

import cv2
import numpy as np

img = cv2.imread('image3.jpg')
# img = cv2.resize(img,(400,500))
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,gray = cv2.threshold(gray,127,255,0)
gray2 = gray.copy()
mask = np.zeros(gray.shape,np.uint8)
contours, hier = cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    if cv2.contourArea(cnt)<500:

        # cv2.drawContours(mask,[cnt],0,0,-1)
        # (x,y,w,h) = cv2.boundingRect(cnt)

        cv2.drawContours(gray2,[cnt],0,0,-3)
        # cv2.rectangle(gray2,(x,y),(x+w,y+h),0,-1)
        # if gray2[y,x]==255:
        #     cv2.rectangle(gray2,(x,y),(x+w,y+h),255,-1)
        # else:
        #     cv2.rectangle(gray2,(x,y),(x+w,y+h),0,-1)
# cv2.imshow('img',img)

cv2.imshow('mask',img)
cv2.imshow('IMG',gray2)
cv2.waitKey(0)
cv2.destroyAllWindows()