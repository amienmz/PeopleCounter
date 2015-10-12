__author__ = 'pc'
from stereovision.calibration import StereoCalibration
import numpy as np
import cv2
import cv2.cv as cv

def nothing(x):
    pass

video1 = cv2.VideoCapture(0) #right
video1.set(3,352)
video1.set(4,288)

video2 = cv2.VideoCapture(1)
video2.set(3,352)
video2.set(4,288)

cv2.namedWindow('Tuner')
cv2.createTrackbar('SADWindowSize','Tuner',5,21,nothing)
cv2.createTrackbar('preFilterType','Tuner',0,255,nothing)
cv2.createTrackbar('preFilterSize','Tuner',0,255,nothing)
cv2.createTrackbar('preFilterCap','Tuner',1,63,nothing)
cv2.createTrackbar('minDisparity','Tuner',16,255,nothing)
cv2.createTrackbar('numberOfDisparities','Tuner',0,255,nothing)
cv2.createTrackbar('textureThreshold','Tuner',0,255,nothing)
cv2.createTrackbar('uniquenessRatio','Tuner',0,255,nothing)
cv2.createTrackbar('speckleRange','Tuner',0,255,nothing)
cv2.createTrackbar('speckleWindowSize','Tuner',0,255,nothing)

c, r = [288,352]
sbm = cv.CreateStereoBMState()
disparity = cv.CreateMat(c, r, cv.CV_32F)
# sbm.SADWindowSize = 9
# sbm.preFilterType = 1
# sbm.preFilterSize = 5
# sbm.preFilterCap = 61
# sbm.minDisparity = -39
# sbm.numberOfDisparities = 112
# sbm.textureThreshold = 507
# sbm.uniquenessRatio= 0
# sbm.speckleRange = 8
# sbm.speckleWindowSize = 0


calibration = StereoCalibration(input_folder='./data')

while(1):
    ret1, frame1 = video1.read()
    ret2, frame2 = video2.read()

    imgL = cv2.cvtColor(frame1,cv2.COLOR_RGB2GRAY)
    imgR = cv2.cvtColor(frame2,cv2.COLOR_RGB2GRAY)

    rectified_pair = calibration.rectify((imgL, imgR))

    gray_left = cv.fromarray(rectified_pair[0])
    gray_right = cv.fromarray(rectified_pair[1])


    SADWindowSize = cv2.getTrackbarPos('SADWindowSize','Tuner')
    if(SADWindowSize%2 == 0 ):
        SADWindowSize = SADWindowSize + 1
    sbm.SADWindowSize = SADWindowSize
    sbm.preFilterType = cv.CV_STEREO_BM_BASIC#cv2.getTrackbarPos('preFilterType','Tuner')
    preFilterSize = cv2.getTrackbarPos('preFilterSize','Tuner')
    if(preFilterSize%2 == 0):
        preFilterSize = preFilterSize + 1
    if(preFilterSize < 5):
        preFilterSize = 5
    sbm.preFilterSize = preFilterSize
    sbm.preFilterCap = cv2.getTrackbarPos('preFilterCap','Tuner')
    sbm.minDisparity = cv2.getTrackbarPos('minDisparity','Tuner')
    numberOfDisparities = cv2.getTrackbarPos('numberOfDisparities','Tuner')
    if(numberOfDisparities == 0):
        numberOfDisparities = 1
    sbm.numberOfDisparities = numberOfDisparities * 16

    sbm.textureThreshold = cv2.getTrackbarPos('textureThreshold','Tuner')
    sbm.uniquenessRatio= cv2.getTrackbarPos('uniquenessRatio','Tuner')
    sbm.speckleRange = cv2.getTrackbarPos('speckleRange','Tuner')
    sbm.speckleWindowSize = cv2.getTrackbarPos('speckleWindowSize','Tuner')

    cv.FindStereoCorrespondenceBM(gray_left, gray_right, disparity, sbm)
    disparity_visual = cv.CreateMat(c, r, cv.CV_8U)
    cv.Normalize(disparity, disparity_visual, 0, 255, cv.CV_MINMAX)
    disparity_visual = np.array(disparity_visual)

    cv2.imshow("Tuner",disparity_visual)

    # cv2.fastNlMeansDenoising(imgR,None,3,7,21)
    # cv2.imshow("2", imgR)
    char = cv2.waitKey(1)
    if (char == 27):
        break

cv2.destroyAllWindows()
