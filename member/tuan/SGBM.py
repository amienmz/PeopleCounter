from stereovision.calibration import StereoCalibration
import cv2
import numpy as np
left_image = cv2.imread('L.png',0)
right_image = cv2.imread('R.png',0)
# from matplotlib import pyplot as plt

def nothing(x):
    pass
#
video1 = cv2.VideoCapture(0)
video1.set(3,640)
video1.set(4,480)

video2 = cv2.VideoCapture(1)
video2.set(3,640)
video2.set(4,480)

# This assumes you've already calibrated your camera and have saved the
# calibration files to disk. You can also initialize an empty calibration and
# calculate the calibration, or you can clone another calibration from one in
# memory
calibration = StereoCalibration(input_folder='./out')

cv2.namedWindow('Tuner')
cv2.createTrackbar('minDisparity','Tuner',0,255,nothing)
cv2.createTrackbar('numDisparities','Tuner',1,16,nothing) # divide by 16
cv2.createTrackbar('SADWindowSize','Tuner',1,21,nothing) #old number
cv2.createTrackbar('P1','Tuner',0,255,nothing) #
cv2.createTrackbar('P2','Tuner',0,255,nothing) # P2>P1
cv2.createTrackbar('disp12MaxDiff','Tuner',0,255,nothing)
cv2.createTrackbar('preFilterCap','Tuner',0,255,nothing)
cv2.createTrackbar('uniquenessRatio','Tuner',0,25,nothing)
cv2.createTrackbar('speckleWindowSize','Tuner',0,200,nothing)
cv2.createTrackbar('speckleRange','Tuner',0,10,nothing) # multiplied by 16



while 1:
    ret1, frame1 = video1.read()
    ret2, frame2 = video2.read()

    imgR = cv2.cvtColor(frame1,cv2.COLOR_RGB2GRAY)
    imgL = cv2.cvtColor(frame2,cv2.COLOR_RGB2GRAY)
    # imgL = cv2.blur(imgL,(15,15))
    # imgR = cv2.blur(imgR,(15,15))

    # Now rectify two images taken with your stereo camera. The function expects
    # a tuple of OpenCV Mats, which in Python are numpy arrays
    rectified_pair = calibration.rectify((imgL, imgR))

    minDisparity = cv2.getTrackbarPos('minDisparity','Tuner')
    numDisparities = cv2.getTrackbarPos('numDisparities','Tuner')
    if numDisparities == 0:
        numDisparities = 1
    numDisparities = numDisparities *16
    SADWindowSize = cv2.getTrackbarPos('SADWindowSize','Tuner')
    if SADWindowSize%2 == 0:
        SADWindowSize = SADWindowSize + 1
    P1 = cv2.getTrackbarPos('P1','Tuner')
    P2 = cv2.getTrackbarPos('P2','Tuner')
    disp12MaxDiff = cv2.getTrackbarPos('disp12MaxDiff','Tuner')
    preFilterCap = cv2.getTrackbarPos('preFilterCap','Tuner')
    uniquenessRatio = cv2.getTrackbarPos('uniquenessRatio','Tuner')
    speckleWindowSize = cv2.getTrackbarPos('speckleWindowSize','Tuner')
    speckleRange = cv2.getTrackbarPos('speckleRange','Tuner')
    fullDP = True

    block_matcher = cv2.StereoSGBM(minDisparity, numDisparities, SADWindowSize, P1, P2,disp12MaxDiff,preFilterCap, uniquenessRatio,speckleWindowSize,speckleRange,fullDP)

    # Compute disparity image

    disparity = block_matcher.compute(rectified_pair[0], rectified_pair[1])

    # norm_coeff = 255 / disparity.max()
    # cv2.imshow("disparity", disparity/225.)
    disparity_visual = cv2.normalize(disparity,disparity, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    # dis = cv2.cvtColor(disparity_visual, cv2.COLOR_RGB2GRAY)
    # mark = np.zeros(imgL.shape[:2], np.uint8)
    # inpain = cv2.inpaint(dis, mark, 3, cv2.INPAINT_TELEA)
    # Show normalized version of image so you can see the values
    display = cv2.medianBlur(disparity_visual,5)
    cv2.imshow("Tuner", display)
    # cv2.imshow("pain", inpain)
    cv2.imshow("image", imgL)
    # cv2.imshow("imageR", imgR)
    char = cv2.waitKey(10)
    if (char == 27):
        break

cv2.destroyAllWindows()