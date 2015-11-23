__author__ = 'pc'
import cv2
import numpy as np

class DetectMoving(object):
    def __init__(self,windowSize):
        self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
        self.windowSize = windowSize
        self.WIDTH_PCONS = 50
        self.HEIGHT_PCONS = 50

    def checkRectDetect(self, startPoint, endPoint, contourSize, widthOfImage, heightOfImage):
        missingHeight = self.windowSize - contourSize[1]
        missingWidth = self.windowSize - contourSize[0]

        if missingHeight % 2 != 0:
            data11= int(missingHeight/2)
            data21 = data11 + 1
        else:
            data21 =data11 = int(missingHeight/2)

        if missingWidth % 2 != 0:
            data10= int(missingWidth/2)
            data20 = data10 + 1
        else:
            data20 =data10= int(missingWidth/2)

        if startPoint[0]-data10 < 0:
            data20 += (data10 - startPoint[0])
            data10 = startPoint[0]
        if startPoint[1]-data11 < 0:
            data21 += (data11 - startPoint[1])
            data11 = startPoint[1]
        # print pon1,pon2
        if endPoint[0]+data20 >= widthOfImage:
            data10 += (data20 - (widthOfImage - endPoint[0]))
            data20 = (widthOfImage - endPoint[0])
        if endPoint[1]+data21 >= heightOfImage:
            data11 += (data21 - (heightOfImage - endPoint[1]))
            data21 = (heightOfImage - endPoint[1])
        return (startPoint[0]-data10,startPoint[1]-data11),(endPoint[0]+data20,endPoint[1]+data21)

    def locRec(seft,pon1,pon2):
        if pon2[1] - pon1[1] < seft.WIDTH_PCONS or pon2[0] - pon1[0] < seft.WIDTH_PCONS:
            return False
        else:
            return True

    def detectObjectInImage(self,image):
        h,w = image.shape
        opening = cv2.morphologyEx(image.copy(),cv2.MORPH_OPEN,self.kernel, iterations = 3)
        re,thresh1 = cv2.threshold(opening,75,255,cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        PosObj = []
        PosObj150 = []
        for cn in contours:
            rect = cv2.boundingRect(cn)
            if cv2.contourArea(cn) > 500:
                # print rect
                # start point (x, y) of window
                startPoint = (rect[0], rect[1])

                # end point (x+w, y+h) of window
                endPoint = (rect[0]+ rect[2],rect[1]+rect[3])

                # (width, height) of window
                contourSize = (rect[2],rect[3])
                # self.CheckRectDetect(ponto1,ponto2,ponto3,w,h)
                # PosObj.append((self.CheckRectDetect(ponto1,ponto2,ponto3,w,h)))
                if self.locRec(startPoint,endPoint):
                    PosObj.append((startPoint,endPoint,contourSize))
                    PosObj150.append((self.checkRectDetect(startPoint,endPoint,contourSize,w,h)))
        return  PosObj,PosObj150