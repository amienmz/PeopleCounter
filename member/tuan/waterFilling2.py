__author__ = 'pc'

import cv2
import numpy as np
import random
import time
start_time = time.time()

# f(x,y)
image = cv2.imread('868.jpg', 0)
image = cv2.resize(image, (image.shape[1]/10, image.shape[0]/10))
height, width = image.shape[:2]

#number of raindrop
k = 100*width * height

# g(x,y)
output = np.zeros(image.shape[:2],dtype=int)

# list neighborhood point
neighborhood = np.array([[0,0,1,1,1,-1,-1,-1], [1,-1,0,-1,1,0,1,-1]], np.int8)

for i in range(k):
    x = random.randint(0, width-1)
    y = random.randint(0, height-1)

    while True:
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
        y_min, x_min = listNeighbor[listd.index(min(listd))]
        if min(listd) < 0:
            x = x_min
            y = y_min
        else:
            output[y,x] = output[y,x] + 1
            break;

print("--- %s seconds ---" % (time.time() - start_time))
# output = output * 50
print output

cv2.imwrite("output.jpg", output)
cv2.imshow("output", output)
np.savetxt("water.txt", output, fmt='%d' ,delimiter='\t')
np.savetxt("image.txt", image, fmt='%d' ,delimiter='\t')
cv2.waitKey(0)




