__author__ = 'pc'
import cv2
import numpy as np
class ObjectMoving(object):
    def __init__(self,width,height,step):
        self.max_width = width
        self.max_height = height
        self.max_step = step

    def getImgObjectMoving(self,image):
        ret, data = cv2.threshold(image.copy(),254,255,cv2.THRESH_BINARY)

        contours, hierarchy = cv2.findContours(data,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        rectx = 9999
        recty = 9999
        rectw = 0
        recth = 0
        res = False
        for cn in contours:
            ver = cv2.boundingRect(cn)
            if cv2.contourArea(cn) > 50:
                res = True
                maiorArea = cv2.contourArea(cn)
                rect = ver
                # print rect
                if rect[0] < rectx:
                    rectx = rect[0]
                if rect[1] < recty:
                    recty = rect[1]
                if rectw < rect[0]+ rect[2]:
                    rectw = rect[0]+ rect[2]
                if recth < rect[1]+ rect[3]:
                    recth = rect[1]+ rect[3]
        if res:
            hrect = recth-recty
            wrect = rectw-rectx
            if hrect < self.max_height:
                if recty - (self.max_height - hrect) < 0:
                    recth += (self.max_height - hrect)
                else:
                    recty -= (self.max_height - hrect)
            if wrect < self.max_width:
                if rectx - (self.max_width - wrect) < 0:
                    rectw += (self.max_width - wrect)
                else:
                    rectx -= (self.max_width - wrect)
            mw = rectw - self.max_width - rectx
            mh = recth - self.max_height - recty

            if mw % self.max_step != 0:
                rectw = self.max_width + mw - mw % self.max_step + rectx
            if mh % self.max_step != 0:
                recth = self.max_height + mh - mh % self.max_step + recty
        return res,(rectx,recty),(rectw,recth)