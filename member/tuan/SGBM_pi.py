from stereovision.calibration import StereoCalibration
import cv2
import numpy as np
import  time

def nothing(x):
    pass

video1 = cv2.VideoCapture(0) #right
video1.set(3,352)
video1.set(4,288)

video2 = cv2.VideoCapture(1)
video2.set(3,352)
video2.set(4,288)

# This assumes you've already calibrated your camera and have saved the
# calibration files to disk. You can also initialize an empty calibration and
# calculate the calibration, or you can clone another calibration from one in
# memory
calibration = StereoCalibration(input_folder='./data')

minDisparity = 8
numDisparities = 3 *16
SADWindowSize = 1 #old number
P1 = 35
P2 = 89
disp12MaxDiff = 0
preFilterCap = 0
uniquenessRatio = 0
speckleWindowSize = 0
speckleRange = 0
fullDP = True

count = 0
while 1:
    start_time = time.time()
    ret1, frame1 = video1.read()
    ret2, frame2 = video2.read()

    imgL = cv2.cvtColor(frame1,cv2.COLOR_RGB2GRAY)
    imgR = cv2.cvtColor(frame2,cv2.COLOR_RGB2GRAY)

    rectified_pair = calibration.rectify((imgL, imgR))

    block_matcher = cv2.StereoSGBM(minDisparity, numDisparities, SADWindowSize, P1, P2,disp12MaxDiff,preFilterCap, uniquenessRatio, speckleWindowSize,speckleRange,fullDP)
    disparity = block_matcher.compute(rectified_pair[0], rectified_pair[1])

    display = cv2.normalize(disparity,disparity, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    # cv2.imshow("Before filter", display)
    (T, mask) = cv2.threshold(display, 0, 255, cv2.THRESH_BINARY_INV)

    display = cv2.medianBlur(display, 5)

    #cv2.imshow("Tuner", display)
    count = count + 1
    print str(count) + " Time: " + str(time.time() - start_time) + " s"

    char = cv2.waitKey(10)
    if (char == 27):
        break

cv2.destroyAllWindows()