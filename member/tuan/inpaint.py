__author__ = 'pc'
import numpy as np
import  cv2

def nothing(x):
    pass

img = cv2.imread("1.png")
# (T, mask) = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
# mask = cv2.cvtColor(mask, cv2.COLOR_RGB2GRAY)

cv2.imshow('before',img)
# cv2.waitKey(0)
# dst = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)

cv2.namedWindow('Tuner')
cv2.createTrackbar('1','Tuner',1,255,nothing) #### 78
cv2.createTrackbar('2','Tuner',1,255,nothing) # divide by 16 = 2

while True:
    # T1 = cv2.getTrackbarPos("1","Tuner")
    # T2 = cv2.getTrackbarPos("2","Tuner")

    # dst = cv2.Canny(img, T1, T2)
    dst = cv2.bilateralFilter(img,11,55,55)
    # dst = cv2.adaptiveBilateralFilter()
    cv2.imshow('Tuner', dst)

    char = cv2.waitKey(10)
    if (char == 27):
        break

cv2.destroyAllWindows()