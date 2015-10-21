__author__ = 'pc'
from source.utils.depthmapCalculator import DepthmapCalculator
from source.utils.videoStreamer import VideoStreamer
import cv2

streamer = VideoStreamer('../Datas/outputL24.avi','../Datas/outputR24.avi')
# videoStreamer = VideoStreamer('localhost', '8888')
videoLeft, videoRight = streamer.get_video_data()
depthmapCalculator = DepthmapCalculator('../Datas/data')
calibration = depthmapCalculator.get_calibration()
block_matcher = depthmapCalculator.get_block_macher()

# if videoStreamer.connect_pi():
while True:
    # image_left, image_right = videoStreamer.get_image_from_pi()
    image_left, image_right = streamer.get_image_from_video(videoLeft,videoRight)
    depthmap = depthmapCalculator.calculate(image_left, image_right, block_matcher, calibration)
    cv2.imshow("depthmap", depthmap)
    char = cv2.waitKey(10)
    if (char == 99):
        cv2.waitKey(0)
    if (char == 27):
        break