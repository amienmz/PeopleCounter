__author__ = 'pc'
from source.utils.depthmapCalculator import DepthmapCalculator
from source.utils.videoStreamer import VideoStreamer
from source.utils.backgroundSubtraction import BackgroundSubtraction
import numpy as np
import cv2

streamer = VideoStreamer('../Datas/outputL24.avi','../Datas/outputR24.avi')
# videoStreamer = VideoStreamer('localhost', '8888')
videoLeft, videoRight = streamer.get_video_data()
depthmapCalculator = DepthmapCalculator('../Datas/data')
calibration = depthmapCalculator.get_calibration()
block_matcher = depthmapCalculator.get_block_macher()
backgroundSubtraction = BackgroundSubtraction()

params = cv2.SimpleBlobDetector_Params()
params.filterByColor = 1
params.blobColor = 150

detector = cv2.SimpleBlobDetector(params)

# if videoStreamer.connect_pi():
count = 0
while True:
    # image_left, image_right = videoStreamer.get_image_from_pi()
    image_left, image_right = streamer.get_image_from_video(videoLeft,videoRight)
    depthmap = depthmapCalculator.calculate(image_left, image_right, block_matcher, calibration)
    # cv2.imshow("depthmap", depthmap)
    display = backgroundSubtraction.compute(depthmap)

    cv2.imshow("back", display)
    char = cv2.waitKey(10)
    if (char == 99):
        count += 1
        cv2.imwrite('capture/img' + str(count)+'.png', display)
        cv2.waitKey(0)
    if (char == 27):
        break