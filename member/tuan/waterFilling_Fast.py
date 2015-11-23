__author__ = 'pc'

import cv2
import numpy as np
import random
import time
start_time = time.time()
# f(x,y)
image = cv2.imread('1810.jpg', 0)
image = cv2.medianBlur(image, 51)
# kernel = np.ones((25,25),np.uint8)
# image = cv2.erode(image,kernel,iterations = 1)
cv2.imshow("i", image)
cv2.waitKey(0)

image = cv2.resize(image, (image.shape[1]/10, image.shape[0]/10))
height, width = image.shape[:2]

# g(x,y)
output = np.zeros(image.shape[:2],dtype=int)

# amount of water in one raindrop
R = 100

#number of raindrop
k = (100 * width * height)/R

# amount of water dropped one time
r = 15

# list neighborhood point
neighborhood = np.array([[0,0,1,1,1,-1,-1,-1], [1,-1,0,-1,1,0,1,-1]], np.int8)

print min([2,3])




for i in range(k):
    x = random.randint(0, width-1)
    y = random.randint(0, height-1)
    w = R
    while w > 0:
        # list store different value between neighbor point
        listd = []
        # list store list (x,y) of neighbor point
        listNeighbor = []
        for t in range(8):
            x_neighbor = x + neighborhood[0,t]
            y_neighbor = y + neighborhood[1,t]
            if x_neighbor < 0 or y_neighbor < 0 or x_neighbor==width or y_neighbor==height:
                continue

            d = image[y_neighbor, x_neighbor] + output[y_neighbor, x_neighbor] - (image[y,x] + output[y,x])
            listd.append(d)
            listNeighbor.append((y_neighbor, x_neighbor))
        min_d = min(listd)
        y_min, x_min = listNeighbor[listd.index(min_d)]
        if min_d + r < 0:
            x = x_min
            y = y_min
        else:
            output[y,x] = output[y,x] + min([r,w])
            w = w -r

print("--- %s seconds ---" % (time.time() - start_time))
# output = output * 50
print output
# output = np.uint8(output)
# (T, output) = cv2.threshold(output, 20, 255, cv2.THRESH_BINARY_INV)
cv2.imwrite("output.jpg", output)
np.savetxt("water.txt", output, fmt='%d' ,delimiter='\t')
# np.savetxt("image.txt", image, fmt='%d' ,delimiter='\t')
cv2.waitKey(0)




