__author__ = 'anhdt'
from stereovision.calibration import StereoCalibration
import cv2
import numpy as np
left_image = cv2.imread('L.png',0)
right_image = cv2.imread('R.png',0)
# from matplotlib import pyplot as plt

def nothing(x):
    pass
#
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


cv2.namedWindow('Tuner')
cv2.createTrackbar('minDisparity','Tuner',0,255,nothing) #### 78
cv2.createTrackbar('numDisparities','Tuner',1,16,nothing) # divide by 16 = 2
cv2.createTrackbar('SADWindowSize','Tuner',1,21,nothing) #old number
cv2.createTrackbar('P1','Tuner',0,255,nothing) # 25
cv2.createTrackbar('P2','Tuner',0,255,nothing) # P2>P1 84
cv2.createTrackbar('disp12MaxDiff','Tuner',0,255,nothing)
cv2.createTrackbar('preFilterCap','Tuner',0,255,nothing)
cv2.createTrackbar('uniquenessRatio','Tuner',0,25,nothing)
cv2.createTrackbar('speckleWindowSize','Tuner',0,200,nothing)
cv2.createTrackbar('speckleRange','Tuner',0,32,nothing) # multiplied by 16

minDisparity = 12
numDisparities = 2 *16
SADWindowSize = 1 #old number
P1 = 19
P2 = 84
disp12MaxDiff = 14
# preFilterCap =
# uniquenessRatio =
# speckleWindowSize =
# speckleRange =
fullDP = True
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(4,4))
fgbg1 = cv2.BackgroundSubtractorMOG2()
fgbg2 = cv2.BackgroundSubtractorMOG2()
while 1:
    ret1, frame1 = video1.read()
    ret2, frame2 = video2.read()

    imgR = cv2.cvtColor(frame1,cv2.COLOR_RGB2GRAY)
    imgL = cv2.cvtColor(frame2,cv2.COLOR_RGB2GRAY)
    # print imgR.shape[:2]
    # imgL = cv2.blur(imgL,(15,15))
    # imgR = cv2.blur(imgR,(15,15))

    # Now rectify two images taken with your stereo camera. The function expects
    # a tuple of OpenCV Mats, which in Python are numpy arrays
    rectified_pair = calibration.rectify((imgL, imgR))
    imgx1 = rectified_pair[0]
    imgx2 = rectified_pair[1]
    rectified_pair[0] = cv2.medianBlur(rectified_pair[0],7)
    rectified_pair[1] = cv2.medianBlur(rectified_pair[1],7)
    fgmask1 = fgbg1.apply(rectified_pair[0])
    fgmask1 = cv2.morphologyEx(fgmask1, cv2.MORPH_OPEN, kernel)
    fgmask2 = fgbg2.apply(rectified_pair[1])
    fgmask2 = cv2.morphologyEx(fgmask1, cv2.MORPH_OPEN, kernel)
    rectified_pair[0] = cv2.bitwise_and(imgx1,imgx1,None,fgmask1)
    rectified_pair[1] = cv2.bitwise_and(imgx2,imgx2,None,fgmask2)
    # cv2.imshow("crop", rectified_pair[0])
    # cv2.waitKey(0)
    #crop image Left
    # hL, wL = rectified_pair[0].shape[0:2]

    # print "w" + str(hL)
    # matrix, roiL = cv2.getOptimalNewCameraMatrix(calibration.cam_mats["left"], calibration.dist_coefs["left"], (wL, hL), 1)
    # xL, yL, wL, hL = roiL
    # rectified_pair[0] = rectified_pair[0][yL:yL+hL,xL:xL+wL]
    # rectified_pair[1] = rectified_pair[1][yL:yL+hL,xL:xL+wL]


    # minDisparity = cv2.getTrackbarPos('minDisparity','Tuner')
    # numDisparities = cv2.getTrackbarPos('numDisparities','Tuner')
    # if numDisparities == 0:
    #     numDisparities = 1
    # numDisparities = numDisparities *16
    # SADWindowSize = cv2.getTrackbarPos('SADWindowSize','Tuner')
    # if SADWindowSize%2 == 0:
    #     SADWindowSize = SADWindowSize + 1
    # P1 = cv2.getTrackbarPos('P1','Tuner')
    # P2 = cv2.getTrackbarPos('P2','Tuner')
    # disp12MaxDiff = cv2.getTrackbarPos('disp12MaxDiff','Tuner')
    preFilterCap = cv2.getTrackbarPos('preFilterCap','Tuner')
    uniquenessRatio = cv2.getTrackbarPos('uniquenessRatio','Tuner')
    speckleWindowSize = cv2.getTrackbarPos('speckleWindowSize','Tuner')
    speckleRange = cv2.getTrackbarPos('speckleRange','Tuner')
    # fullDP = True

    block_matcher = cv2.StereoSGBM(minDisparity, numDisparities, SADWindowSize, P1, P2,disp12MaxDiff,preFilterCap, uniquenessRatio, speckleWindowSize,speckleRange,fullDP)

    # Compute disparity image

    disparity = block_matcher.compute(rectified_pair[0], rectified_pair[1])
    # disparity = block_matcher.compute(imgL, imgR)



    # norm_coeff = 255 / disparity.max()
    # cv2.imshow("disparity", disparity/225.)
    disparity_visual = cv2.normalize(disparity,disparity, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)


    # small_depth = cv2.resize(disparity_visual, (0,0), disparity_visual, 0.2, 0.2)
    mark = np.zeros(disparity_visual.shape[:2], np.uint8)
    display = cv2.inpaint(disparity_visual, mark, 10, cv2.INPAINT_TELEA, disparity_visual)
    # (T, mask) = cv2.threshold(display, 200, 255, cv2.THRESH_BINARY)
    # mask = cv2.cvtColor(mask, cv2.COLOR_RGB2GRAY)
    # dst = cv2.inpaint(display, mask, 3, cv2.INPAINT_TELEA)

    # dis = cv2.cvtColor(disparity_visual, cv2.COLOR_RGB2GRAY)
    # mark = np.zeros(imgL.shape[:2], np.uint8)
    # inpain = cv2.inpaint(dis, mark, 3, cv2.INPAINT_TELEA)
    # Show normalized version of image so you can see the values
    # display = cv2.medianBlur(disparity_visual,5)
    # display = display[yL:yL+hL,xL:xL+wL]
    display = cv2.medianBlur(display, 11)
    cv2.imshow("Tuner", display)
    # cv2.imshow("mask", mask)
    # cv2.imshow("Tuner", disparity_visual)
    # cv2.imshow("pain", inpain)
    # cv2.imshow("image", imgL)
    # cv2.imshow("res",rectified_pair[0])
    # cv2.imshow("res2",rectified_pair[1])
    # cv2.imshow("imageR", imgR)
    char = cv2.waitKey(10)
    if (char == 27):
        break

cv2.destroyAllWindows()