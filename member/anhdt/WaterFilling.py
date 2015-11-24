from numpy.f2py.auxfuncs import throw_error

__author__ = 'pc'
import cv2
import numpy as np
import time
start_time = time.time()

def CheckRectDetect(pon1,pon2,pon3,w,h):
        datah = 150 - pon3[1]
        dataw = 150 - pon3[0]
        if datah % 2 != 0:
            data11= int(datah/2)
            data21 = data11 + 1
        else:
            data21 =data11 = int(datah/2)
        if dataw % 2 != 0:
            data10= int(dataw/2)
            data20 = data10 + 1
        else:
            data20 =data10= int(dataw/2)

        if pon1[0]-data10 < 0:
            data20 += (data10 - pon1[0])
            data10 = pon1[0]
        if pon1[1]-data11 < 0:
            data21 += (data11 - pon1[1])
            data11 = pon1[1]
        # print pon1,pon2
        if pon2[0]+data20 >= w:
            data10 += (data20 - (w - pon2[0]))
            data20 = (w - pon2[0])
        if pon2[1]+data21 >= h:
            data11 += (data21 - (h - pon2[1]))
            data21 = (h - pon2[1])
        return (pon1[0]-data10,pon1[1]-data11),(pon2[0]+data20,pon2[1]+data21)


threshHold = 5

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

image = cv2.imread('3787.jpg', 0)
image = cv2.medianBlur(image, 31)
# (T, image) = cv2.threshold(image, image.max()-20, 255, cv2.THRESH_BINARY)

# image = cv2.Canny(image, 20,20)
imagex = image.copy()
cv2.imshow("image", image)
cv2.waitKey(0)

image = cv2.resize(image, (image.shape[1]/20, image.shape[0]/20))

height, width = image.shape[:2]

print width

output = np.ones(image.shape[:2], dtype=int) * (np.nan)
output[0,0] = 0
print output[0,0] == np.nan
print np.isnan(output[0,0])

# cv2.imshow("output", output)

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
print output
(T, output) = cv2.threshold(output, 1, 255, cv2.THRESH_BINARY)
output = cv2.medianBlur(output, 3)
print output
contours, hierarchy = cv2.findContours(output,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for cn in contours:
    ver = cv2.boundingRect(cn)
    if cv2.contourArea(cn) > 0:
        maiorArea = cv2.contourArea(cn)
        rect = ver
        # print rect
        ponto1 = (rect[0]*20, rect[1]*20)
        ponto2 = ((rect[0]+ rect[2])*20,(rect[1]+rect[3])*20)
        ponto3 = (ponto2[0]-ponto1[0],ponto2[1]-ponto1[1])
        cv2.rectangle(imagex, ponto1, ponto2,(255,255,255), 2)
        data1,data2 = CheckRectDetect(ponto1,ponto2,ponto3,352,288)
        cv2.rectangle(imagex, data1, data2,(255,255,255), 1)

# output = output * 100
# output = np.uint8(output)
cv2.imshow("image", imagex)
cv2.waitKey(0)

cv2.imwrite("output.jpg", output)
cv2.imshow("output", output)
# np.savetxt("water.txt", output, fmt='%d' ,delimiter='\t')
# np.savetxt("image.txt", image, fmt='%d' ,delimiter='\t')

# cv2.waitKey(0)