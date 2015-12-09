__author__ = 'pc'

import cv2
import numpy as np
import time

start_time = time.time()
# Variable
threshHold = 40
noiseSize = 3000
x = 1
listHead = []
lastNumberOfContour = 0

image = cv2.imread('1810.jpg', 0)
image = cv2.medianBlur(image, 31)
cv2.imshow("image", image)
cv2.waitKey(0)
height, width = image.shape[:2]



image = (image/threshHold)*threshHold
cv2.imshow("i", image)
cv2.waitKey(0)
lastSum = 0
while True:
    (T, imageCopy) = cv2.threshold(image.copy(), image.max()-(threshHold * x), 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(imageCopy.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    if np.sum(imageCopy) == (255*imageCopy.shape[1]*imageCopy.shape[0]):
    # if np.sum(imageCopy) == lastSum:
        break
    lastSum = np.sum(imageCopy)
    (T, imageCopy) = cv2.threshold(image.copy(), image.max()-(threshHold * (x-1)), 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(imageCopy.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    if len(listHead) == 0:
        for cn in contours:
            print "size: " + str(cv2.contourArea(cn))
            if cv2.contourArea(cn) > noiseSize:
                M = cv2.moments(cn)
                centroid_x = int(M['m10']/M['m00'])
                centroid_y = int(M['m01']/M['m00'])
                listHead.append((centroid_x, centroid_y))
    else:
        isExistContour = False
        # check if have any head position in contour
        for cn in contours:
            for headPosition in listHead:
                if cv2.pointPolygonTest(cn, headPosition, True) >= 0:
                    isExistContour = True
                    break
                else:
                    isExistContour = False
            # if contour dont wrap any head position, add that contour to new listHead
            if not isExistContour:
                print "size: " + str(cv2.contourArea(cn))
                if cv2.contourArea(cn) > noiseSize:
                    M = cv2.moments(cn)
                    centroid_x = int(M['m10']/M['m00'])
                    centroid_y = int(M['m01']/M['m00'])
                    listHead.append((centroid_x, centroid_y))

    for point in listHead:
        cv2.circle(imageCopy, point, 5, (0,0,0))

    lastNumberOfContour = len(contours)

    x +=1
    cv2.imshow("i", imageCopy)
    cv2.waitKey(0)
print("--- %s seconds ---" % (time.time() - start_time))
print listHead
