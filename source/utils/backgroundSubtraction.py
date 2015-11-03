__author__ = 'pc'
import cv2
import numpy as np
class BackgroundSubtraction(object):
    def __init__(self):
        self.fgbg = cv2.BackgroundSubtractorMOG2(history=10, varThreshold=100, bShadowDetection=1)
        pass


    def is_contour_bad(self, c):
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.1 * peri, True)

        # the contour is 'bad' if it is not a rectangle
        return cv2.contourArea(c)<5000

    def compute(self, image):
        fgmask = self.fgbg.apply(image, learningRate=0)
        contours, hiararchy = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        maskBad = np.ones(fgmask.shape[:2], dtype="uint8") * 255
        maskGood = np.ones(fgmask.shape[:2], dtype="uint8")

        for c in contours:
            if self.is_contour_bad(c):
                cv2.drawContours(maskBad, [c], -1, 0, -1)

        #remove bad contour (small contour)
        fgmask = cv2.bitwise_and(fgmask, fgmask, mask=maskBad)

        # fill hole in image
        contours, hiararchy = cv2.findContours(fgmask.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            cv2.drawContours(maskGood, [c], 0, 255, -1)
        return maskGood, cv2.bitwise_and(image, maskGood)

