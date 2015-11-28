__author__ = 'pc'
import cv2
import numpy as np

class DetectMoving(object):
    def __init__(self,sizeImg):
        self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
        self.sizeImg = sizeImg
        self.WIDTH_PCONS = 50
        self.HEIGHT_PCONS = 50
        self.noiseSize = 700
        self.threshHold = 40

    def compare(self,a, b):
        a = np.int(a)
        b = np.int(b)
        if abs(a-b) <= self.threshHold:
            return 0
        if (b-a) > self.threshHold:
            return 1
        else:
            return -1

    def resize4detect(self,pon1,pon2,pon3,w,h):
        datah = 50 - pon3[1]
        dataw = 60 - pon3[0]
        data11 = data10 = data20 = data21 = 0
        if datah < 0 or dataw < 0:
            if datah < 0:
                datah1 = -datah
                if datah1 % 2 != 0:
                    data11= int(datah1/2)
                    data21 = data11 + 1
                else:
                    data21 =data11 = int(datah1/2)
                if dataw >= 0:
                    if dataw % 2 != 0:
                        data10= int(dataw/2)
                        data20 = data10 + 1
                    else:
                        data20 =data10= int(dataw/2)
                    if pon1[0]-data10 < 0:
                        data20 += (data10 - pon1[0])
                        data10 = pon1[0]
                    if pon2[0]+data20 >= w:
                        data10 += (data20 - (w - pon2[0]))
                        data20 = (w - pon2[0])
                    return (pon1[0]-data10,pon1[1]+data11),(pon2[0]+data20,pon2[1]-data21)
            if dataw < 0:
                dataw1 = -dataw
                if dataw1 % 2 != 0:
                    data10= int(dataw1/2)
                    data20 = data10 + 1
                else:
                    data20 =data10= int(dataw1/2)
                if datah >= 0:
                    if datah % 2 != 0:
                        data11= int(datah/2)
                        data21 = data11 + 1
                    else:
                        data21 =data11 = int(datah/2)
                    if pon1[1]-data11 < 0:
                        data21 += (data11 - pon1[1])
                        data11 = pon1[1]
                    if pon2[1]+data21 >= h:
                        data11 += (data21 - (h - pon2[1]))
                        data21 = (h - pon2[1])
                    return (pon1[0]+data10,pon1[1]-data11),(pon2[0]-data20,pon2[1]+data21)
            return (pon1[0]+data10,pon1[1]+data11),(pon2[0]-data20,pon2[1]-data21)
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

    def detectObjectInImage(self,img):
        h,w = img.shape
        image = img.copy()
        x = 1
        listHead = []
        image = cv2.medianBlur(image, 31)
        image = (image/self.threshHold)*self.threshHold
        while True:
            (T, imageCopy) = cv2.threshold(image.copy(), image.max()-(self.threshHold * x), 255, cv2.THRESH_BINARY)
            if np.sum(imageCopy) == (255*imageCopy.shape[1]*imageCopy.shape[0]):
                break

            (T, imageCopy) = cv2.threshold(image.copy(), image.max()-(self.threshHold * (x-1)), 255, cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(imageCopy.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            if len(listHead) == 0:
                for cn in contours:
                    if cv2.contourArea(cn) > self.noiseSize:
                        M = cv2.moments(cn)
                        centroid_x = int(M['m10']/M['m00'])
                        centroid_y = int(M['m01']/M['m00'])
                        listHead.append((centroid_x, centroid_y))
            else:
                isExistContour = False
                # check if have any head position in contour
                for cn in contours:
                    for headPosition in listHead:
                        if cv2.pointPolygonTest(cn, headPosition, True) >= 0:
                            isExistContour = True
                            break
                        else:
                            isExistContour = False
                    # if contour dont wrap any head position, add that contour to new listHead
                    if not isExistContour:
                        if cv2.contourArea(cn) > self.noiseSize:
                            M = cv2.moments(cn)
                            centroid_x = int(M['m10']/M['m00'])
                            centroid_y = int(M['m01']/M['m00'])
                            listHead.append((centroid_x, centroid_y))
            x +=1
        PosObj = []
        PosObj150 = []
        for cn in listHead:
            datax,datay = self.resize4detect(cn,cn,(0,0),w,h)
            PosObj.append((datax,datay,(datay[0]-datax[0],datay[1]-datax[1])))
            PosObj150.append((self.CheckRectDetect(cn,cn,(0,0),w,h)))
        return  PosObj, PosObj150