__author__ = 'pc'
from skimage.feature import hog
import cv2
import numpy as np
# img = cv2.imread("../../data/dataset/pos/pos-1.png")
img = cv2.imread('91.jpg')
print img.shape
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img = img[0:285,0:345]
# img = img[0:150,0:150]
fd,imgx = hog(img, 8, (15, 15), (1, 1), True)
# for x in range(285):
#     for y in range(345):
#         dx = fd[x:800]
#
#         pass

# for x in range(285):
# for y in range(195):
#     dataa = []
#     indx = y+79
#     indy = y
#     for size in range(10):
#         # dataa.append(fd[indy:indx])
#         fd[indy:indx]
#         indy = indx+105
#         indx = indy+79

print img.shape
print fd
print len(fd)

print (135/15)*(135/15)*8
# np.savetxt("m.txt",fd)
cv2.imshow("y",imgx)
cv2.imshow("x",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
