__author__ = 'pc'
import numpy as np
import  cv2

img = cv2.imread("paint.png")
(T, mask) = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
mask = cv2.cvtColor(mask, cv2.COLOR_RGB2GRAY)

cv2.imshow('mask',mask)
cv2.waitKey(0)
dst = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)

cv2.imshow('dst', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()