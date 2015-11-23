__author__ = 'pc'
from source.stereovision.calibration import StereoCalibration
import cv2

class DepthmapCalculator(object):

    def __init__(self, data):
        self.link_data = data
        self.minDisparity = 15
        self.numDisparities = 3 *16
        self.SADWindowSize = 1
        self.P1 = 32
        self.P2 = 93
        self.disp12MaxDiff = 0
        self.preFilterCap = 0
        self.uniquenessRatio = 0
        self.speckleWindowSize = 0
        self.speckleRange = 0
        self.fullDP = True

    def get_calibration(self):
        return StereoCalibration(input_folder=self.link_data)

    def get_block_macher(self):
        return cv2.StereoSGBM(self.minDisparity,
                              self.numDisparities,
                              self.SADWindowSize,
                              self.P1,
                              self.P2,
                              self.disp12MaxDiff,
                              self.preFilterCap,
                              self.uniquenessRatio,
                              self.speckleWindowSize,
                              self.speckleRange,
                              self.fullDP)

    def calculate(self, left_image, right_image, block_matcher, calibration):

        #convert image to GrayScale
        imgL = cv2.cvtColor(left_image,cv2.COLOR_RGB2GRAY)
        imgR = cv2.cvtColor(right_image,cv2.COLOR_RGB2GRAY)

        #calculator depth map
        rectified_pair = calibration.rectify((imgL, imgR))
        disparity = block_matcher.compute(rectified_pair[0], rectified_pair[1])

        #convert to image
        depthmap = cv2.normalize(disparity,disparity, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

        return depthmap
