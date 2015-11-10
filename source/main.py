__author__ = 'pc'
from source.utils.depthmapCalculator import DepthmapCalculator
from source.utils.videoStreamer import VideoStreamer
from source.utils.backgroundSubtraction import BackgroundSubtraction
from source.utils.ObjectMoving import ObjectMoving
from source.utils.detectObject import DetectMoving
from source.utils.trackingObject import TrackingObj
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

#init tracking
trackObj = TrackingObj()

# subtract moving object
imgObjectMoving = ObjectMoving(150,150,30)

detectMoving = DetectMoving(150)

# if videoStreamer.connect_pi():
count = 0
font = cv2.FONT_HERSHEY_SIMPLEX
cdetect = 0
while True:
    # image_left, image_right = videoStreamer.get_image_from_pi()
    image_left, image_right = streamer.get_image_from_video(videoLeft,videoRight)
    depthmap = depthmapCalculator.calculate(image_left, image_right, block_matcher, calibration)
    # cv2.imshow("depthmap", depthmap)
    if count > 1:
        mask, display = backgroundSubtraction.compute(depthmap)
        # cv2.imshow("back1", mask)
        # res,pon1,pon2 = imgObjectMoving.getImgObjectMoving(mask)
        # if res:
        #     # cv2.rectangle(display,pon1, pon2,(255,255,255), 2)
        #     if count>74:
        #         im_detected = detector.detect(display[pon1[1]:pon2[1],pon1[0]:pon2[0]])
        #     # cv2.imshow("back", display)
        #         cv2.imshow("back", im_detected)
        trackObj.resetTracking()
        data = detectMoving.detectObjectInImage(display)
        if len(data) > 0:
            for x in data:
                # print x[0], x[1]
                # print x[1][0] - x[0][0], x[1][1] - x[0][1]
                # ckObj = trackObj.check_Obj(x[0],x[2])
                # if ckObj == False:
                #     cdetect+=1
                #     print cdetect
                    if detector.detect1(display,x[0],x[1],x[2]):
                        trackObj.trackingObj(x[0],x[2])
                        cv2.rectangle(display,x[0], x[1],(255,255,255), 2)
                # else:
                #     cv2.rectangle(display,x[0], x[1],(255,255,255), 2)
        trackObj.remove_track()
        cv2.line(display,(0,20),(352,20),(255,255,255),1)
        cv2.line(display,(0,150),(352,150),(255,255,255),1)
        cv2.line(display,(0,270),(352,270),(255,255,255),1)
        cv2.putText(display,'In: %i'%trackObj.InSh,(50,180), font, 0.5,(255,255,255),1)
        cv2.putText(display,'Out: %i'%trackObj.OutSh,(200,180), font, 0.5,(255,255,255),1)
        cv2.imshow("back", display)

    # print "-----------------------------" + str(count)

    # if res:
    #     cv2.rectangle(display,pon1, pon2,(255,255,255), 2)

    count+=1
    char = cv2.waitKey(1)
    if (char == 99):
    #     count += 1
    #     cv2.imwrite(str(count)+'.jpg', display)
        print trackObj.InSh,trackObj.OutSh
        cv2.waitKey(0)
    if (char == 27):
        break