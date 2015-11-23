from numpy.f2py.auxfuncs import throw_error

__author__ = 'pc'
import cv2
import numpy as np
import time
start_time = time.time()

threshHold = 13

def compare(a, b):
    a = np.int(a)
    b = np.int(b)
    if abs(a-b) <= threshHold:
        return 0
    if (b-a) > threshHold:
        return 1
    else:
        return -1



# near = np.array([[0,1,0,-1], [1,0,-1,0]], np.int8)
near = np.array([[0,0,1,1,1,-1,-1,-1], [1,-1,0,-1,1,0,1,-1]], np.int8)
# near = np.array([[0,1],[1,0],[0,-1],[-1,0]], np.int8)

image = cv2.imread('3794.jpg', 0)
image = cv2.medianBlur(image, 51)
# (T, image) = cv2.threshold(image, image.max()-20, 255, cv2.THRESH_BINARY)

# image = cv2.Canny(image, 20,20)

cv2.imshow("image", image)
cv2.waitKey(0)

image = cv2.resize(image, (image.shape[1]/20, image.shape[0]/20))

height, width = image.shape[:2]

print width

output = np.ones(image.shape[:2], dtype=int) * (np.nan)
output[0,0] = 0
print output[0,0] == np.nan
print np.isnan(output[0,0])

cv2.imshow("output", output)

print output.shape


for y in range(height):
    for x in range(width):
        # print "--------------"
        for t in range(8):
            x_next = x + near[0,t]
            y_next = y + near[1,t]
            if x_next < 0 or y_next < 0 or x_next==width or y_next==height:
                continue
            # print t

            if compare(image[y,x], image[y_next, x_next]) == 0:
                output[y_next, x_next] = output[y,x]

            elif compare(image[y,x], image[y_next, x_next]) == 1:
                if np.isnan(output[y_next, x_next]):
                    output[y_next, x_next] = output[y,x] + 1
                    continue
                if abs(output[y_next, x_next] - output[y,x]) < 2:
                    output[y_next, x_next] = output[y,x] + 1
                    # print output[y_next, x_next]


            elif compare(image[y,x], image[y_next, x_next]) == -1:
                if np.isnan(output[y_next, x_next]):
                    output[y_next, x_next] = output[y,x] -1
                    if(output[y_next, x_next]< 0):
                        output[y_next, x_next] = 0
                    continue
                if abs(output[y_next, x_next] - output[y,x]) < 2 and output[y,x] > 0:
                    output[y_next, x_next] = output[y,x] - 1
                    # print output[y_next, x_next]
                    if(output[y_next, x_next] == -1):
                        pass
                    # if(output[y_next, x_next]< 0):
                    #     output[y_next, x_next] = 0

            # print "[" + str(y) + "," + str(x) + "] "+ str(image[y,x]) + "  : " + str(y_next) + "," + str(x_next) + " : " +str(image[y,x]) +" | "+ str(output[y_next, x_next])

output = np.uint8(output)
# output = cv2.cvtColor(output, cv2.COLOR_RGB2GRAY)
print("--- %s seconds ---" % (time.time() - start_time))
(T, output) = cv2.threshold(output, 1, 255, cv2.THRESH_BINARY)
# output = output * 100
# output = np.uint8(output)
print output
cv2.imwrite("output.jpg", output)
cv2.imshow("output", output)
np.savetxt("water.txt", output, fmt='%d' ,delimiter='\t')
np.savetxt("image.txt", image, fmt='%d' ,delimiter='\t')

# cv2.waitKey(0)