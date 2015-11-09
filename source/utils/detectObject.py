__author__ = 'pc'
import cv2
import numpy as np

class DetectMoving(object):
    def __init__(self,sizeImg):
        self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
        self.sizeImg = sizeImg
        self.WIDTH_PCONS = 50
        self.HEIGHT_PCONS = 50

    def CheckRectDetect(self,pon1,pon2,pon3,w,h):
        datah = self.sizeImg - pon3[1]
        dataw = self.sizeImg - pon3[0]
        if datah % 2 != 0:
            data11= int(datah/2)
            data21 = data11 + 1
        else:
            data21 =data11 = int(datah/2)
        if dataw % 2 != 0:
            data10= int(dataw/2)
            data20 = data10 + 1
        else:
            data20 =data10= int(dataw/2)

        if pon1[0]-data10 < 0:
            data20 += (data10 - pon1[0])
            data10 = pon1[0]
        if pon1[1]-data11 < 0:
            data21 += (data11 - pon1[1])
            data11 = pon1[1]
        # print pon1,pon2
        if pon2[0]+data20 >= w:
            data10 += (data20 - (w - pon2[0]))
            data20 = (w - pon2[0])
        if pon2[1]+data21 >= h:
            data11 += (data21 - (h - pon2[1]))
            data21 = (h - pon2[1])
        return (pon1[0]-data10,pon1[1]-data11),(pon2[0]+data20,pon2[1]+data21)
    def locRec(seft,pon1,pon2):
        if pon2[1] - pon1[1] < seft.WIDTH_PCONS or pon2[0] - pon1[0] < seft.WIDTH_PCONS:
            return False
        else:
            return True
    def detectObjectInImage(self,image):
        # h,w = image.shape
        opening = cv2.morphologyEx(image.copy(),cv2.MORPH_OPEN,self.kernel, iterations = 3)
        re,thresh1 = cv2.threshold(opening,75,255,cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        PosObj = []
        for cn in contours:
            ver = cv2.boundingRect(cn)
            if cv2.contourArea(cn) > 500:
                maiorArea = cv2.contourArea(cn)
                rect = ver
                # print rect
                ponto1 = (rect[0], rect[1])
                ponto2 = (rect[0]+ rect[2],rect[1]+rect[3])
                ponto3 = (rect[2],rect[3])
                # self.CheckRectDetect(ponto1,ponto2,ponto3,w,h)
                # PosObj.append((self.CheckRectDetect(ponto1,ponto2,ponto3,w,h)))
                if self.locRec(ponto1,ponto2):
                    PosObj.append((ponto1,ponto2,ponto3))
        return  PosObj