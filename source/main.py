__author__ = 'pc'
from source.utils.depthmapCalculator import DepthmapCalculator
from source.utils.videoStreamer import VideoStreamer
from source.utils.backgroundSubtraction import BackgroundSubtraction
from source.utils.ObjectMoving import ObjectMoving
import numpy as np
import cv2
from source.learningMachine.detect import Detector

# load video demo
streamer = VideoStreamer('../data/outputL24.avi','../data/outputR24.avi')
# videoStreamer = VideoStreamer('localhost', '8888')

# get video left and right
videoLeft, videoRight = streamer.get_video_data()

# load calibration data to calculate depth map
depthmapCalculator = DepthmapCalculator('../data/calibration')

# calibrate camera
calibration = depthmapCalculator.get_calibration()

# init block matcher (SGBM) to calculate depth map
block_matcher = depthmapCalculator.get_block_macher()

# init background subtraction
backgroundSubtraction = BackgroundSubtraction()

# init detector
detector = Detector(min_window_size=(150, 150), step_size=(30, 30), downscale=1)

# subtract moving object
imgObjectMoving = ObjectMoving(150,150,10)


# if videoStreamer.connect_pi():
count = 0
while True:
    # image_left, image_right = videoStreamer.get_image_from_pi()
    image_left, image_right = streamer.get_image_from_video(videoLeft,videoRight)
    depthmap = depthmapCalculator.calculate(image_left, image_right, block_matcher, calibration)
    # cv2.imshow("depthmap", depthmap)
    if count > 1:
        mask, display = backgroundSubtraction.compute(depthmap)
        # cv2.imshow("back1", mask)
        if count>74:
            im_detected = detector.detect(display)
        # cv2.imshow("back", display)
            cv2.imshow("back", im_detected)
    # print "-----------------------------" + str(count)


    # res,pon1,pon2 = imgObjectMoving.getImgObjectMoving(mask)
    # if res:
    #     cv2.rectangle(display,pon1, pon2,(255,255,255), 2)
    # cv2.imshow("back", display)
    count+=1
    char = cv2.waitKey(1)
    if (char == 99):
    #     count += 1
    #     cv2.imwrite('capture/img' + str(count)+'.png', display)
        cv2.waitKey(0)
    if (char == 27):
        break