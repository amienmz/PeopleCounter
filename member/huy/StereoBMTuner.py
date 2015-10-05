from stereovision.calibration import StereoCalibration
import cv2
left_image = cv2.imread('L.png',0)
right_image = cv2.imread('R.png',0)
# from matplotlib import pyplot as plt

def nothing(x):
    pass
#
video1 = cv2.VideoCapture(0)
video1.set(3,400)
video1.set(4,400)

video2 = cv2.VideoCapture(2)
video2.set(3,400)
video2.set(4,400)

# This assumes you've already calibrated your camera and have saved the
# calibration files to disk. You can also initialize an empty calibration and
# calculate the calibration, or you can clone another calibration from one in
# memory
calibration = StereoCalibration(input_folder='./export')

cv2.namedWindow('Tuner')
cv2.createTrackbar('Campresent','Tuner',0,3,nothing)
cv2.createTrackbar('numDis','Tuner',0,160,nothing)
cv2.createTrackbar('window_size','Tuner',0,21,nothing)
cv2.createTrackbar('PreFilterCap','image',1,63,nothing)
cv2.createTrackbar('PreFilterSize','image',5,255,nothing)
cv2.createTrackbar('PreFilterType','image',0,1,nothing)
while 1:
    ret1, frame1 = video1.read()
    ret2, frame2 = video2.read()

    imgL = cv2.cvtColor(frame1,cv2.COLOR_RGB2GRAY)
    imgR = cv2.cvtColor(frame2,cv2.COLOR_RGB2GRAY)

    # Now rectify two images taken with your stereo camera. The function expects
    # a tuple of OpenCV Mats, which in Python are numpy arrays
    rectified_pair = calibration.rectify((imgL, imgR))

    _bm_preset = cv2.getTrackbarPos('Campresent','Tuner')
    _search_range = cv2.getTrackbarPos('numDis','Tuner')
    _window_size = cv2.getTrackbarPos('window_size','Tuner')

    if _window_size<5:
        _window_size=5

    if _window_size % 2 == 0:
        _window_size+=1

    _search_range=_search_range*16

    block_matcher = cv2.StereoBM(preset=_bm_preset,
                                          ndisparities=_search_range,
                                          SADWindowSize=_window_size)
    # Compute disparity image

    disparity = block_matcher.compute(rectified_pair[0], rectified_pair[1])

    # norm_coeff = 255 / disparity.max()
    # cv2.imshow("disparity", disparity * norm_coeff / 255)
    disparity_visual = cv2.normalize(disparity,disparity, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    # Show normalized version of image so you can see the values
    cv2.imshow("StereoBMTuner", disparity_visual)
    char = cv2.waitKey(10)
    print str(_bm_preset) +' - '+ str(_search_range) +' - '+ str(_window_size)
    if (char == 27):
        break

cv2.waitKey(1000000)