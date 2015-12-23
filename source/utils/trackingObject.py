import time
from source.utils import const

__author__ = 'pc'
import cv2
import numpy as np
from Object import Object

X = 0
Y = 1
rad = 25


class TrackingObj(object):
    def __init__(self, queue_update_pc, queue_post2web):
        self.allObj = []
        self.InSh = 0
        self.OutSh = 0
        self.maxNumberLostFrame = 10
        self.topPosition = 144 - 70
        self.midPosition = 144
        self.botPosition = 144 + 70
        self.queue_update_pc = queue_update_pc
        self.queue_post2web = queue_post2web

    def resetTracking(self):
        for data in self.allObj:
            data.ClearExist()
            data.clearTemp()
        return None

    def remove_track(self):
        for data in self.allObj:
            if not data.isExist:
                if self.check_withLine(data.y, data.r) is None:
                    self.allObj.remove(data)
                elif data.numberLostFrame < self.maxNumberLostFrame:
                    data.AddFramePass()
                else:
                    self.allObj.remove(data)
        return None

    def sysn_line(self, data, y, rad):
        ln = self.check_withLine(y, rad)
        if ln == 1:
            data.InLineCenter()
            return False, ln
        else:
            data.UpdateLinePass(ln)
            return True, ln

    def check_withLine(self, y, rad):
        if y - rad <= self.topPosition <= y + rad:
            return 0

        if y - rad <= self.botPosition <= y + rad:
            return 2

        if self.topPosition < y - rad and self.botPosition > y + rad:
            return 1

        return None

    def trackingObj(self, pon1, pon2, rad):
        y, x = [pon1[1] + pon2[1] / 2, pon1[0] + pon2[0] / 2]

        # sort listobject by noNumberLostFrame
        self.allObj.sort(key=lambda x: x.numberLostFrame, reverse=False)

        # print x,y,w,h
        haveline = False
        if len(self.allObj) == 0:
            obj = Object(x, y, rad, True)
            self.allObj.append(obj)
            return None

        for data in self.allObj:
            if data.CheckObject(x, y):
                data.UpdateTracking(x, y)
                res, ln = self.sysn_line(data, y, rad)
                if res:
                    inout = data.CheckInOut(ln)
                    if inout == 0:
                        self.OutSh += 1
                        self.queue_update_pc.put(const.TYPE_OUT)
                        self.queue_post2web.put(const.TYPE_OUT)
                    elif inout == 1:
                        self.InSh += 1
                        self.queue_update_pc.put(const.TYPE_IN)
                        self.queue_post2web.put(const.TYPE_IN)
                haveline = True
                break
        if haveline == False:
            obj = Object(x, y, rad, True)
            self.allObj.append(obj)
        return None

    def trackingAllObject(self, arrPointObject):

        if len(self.allObj) == 0:
            for newPoint in arrPointObject:
                obj = Object(newPoint[X], newPoint[Y], rad, True)
                self.allObj.append(obj)
                return

        # print '()()()()()()()()()()()()()()()()(()'
        count =0
        while not (len(arrPointObject) == 0 or self.isAllOldPointMapped()):
            count += 1
            if count > 100:
                break
            # print '--------------'
            # print 'len(arrNew) = ' + str(len(arrPointObject)) + ' isAllMapped = ' + str(self.isAllOldPointMapped())
            newPoint = arrPointObject[0]
            # print '1'
            minLength = 9999
            tempLastPoint = None
            for lastPoint in self.allObj:
                if isinstance(lastPoint, Object):
                    lenth = lastPoint.calculatorDistanceToPoint(newPoint)
                    # print 'len = ' + str(lenth) + ' minLen ' + str(minLength)
                    if lenth < minLength:
                        # print '1b'
                        minLength = lenth
                        tempLastPoint = lastPoint
            if not tempLastPoint is None:
                # print '1c'
                # print 'lastPoint MinLen = ' + str(tempLastPoint.tempMinDistance)
                if not tempLastPoint.tempNextPoint is None:
                    # print '1d'
                    if minLength < tempLastPoint.tempMinDistance:
                        arrPointObject.append(tempLastPoint.tempNextPoint)
                        tempLastPoint.tempNextPoint = newPoint
                        tempLastPoint.tempMinDistance = minLength
                        arrPointObject.remove(newPoint)
                else:
                    # print '1e'
                    tempLastPoint.tempNextPoint = newPoint
                    tempLastPoint.tempMinDistance = minLength
                    arrPointObject.remove(newPoint)
        # print '2'
        for newPoint in arrPointObject:
            obj = Object(newPoint[X], newPoint[Y], rad, True)
            self.allObj.append(obj)

        # print '3'
        for lastPoint in self.allObj:
            if isinstance(lastPoint, Object):
                if lastPoint.tempNextPoint is None:
                    lastPoint.AddFramePass()
                else:
                    if (lastPoint.numberLostFrame<2 and lastPoint.tempMinDistance <= 2*rad) or (lastPoint.numberLostFrame>1 and lastPoint.tempMinDistance <= 4*rad):
                        lastPoint.updateObject()
                        res, ln = self.sysn_line(lastPoint, lastPoint.y, rad)
                        if res:
                            inout = lastPoint.CheckInOut(ln)
                            if inout == 0:
                                self.OutSh += 1
                                self.queue_update_pc.put(const.TYPE_OUT)
                                self.queue_post2web.put(const.TYPE_OUT)
                            elif inout == 1:
                                self.InSh += 1
                                self.queue_update_pc.put(const.TYPE_IN)
                                self.queue_post2web.put(const.TYPE_IN)
                    else:
                        print '>distance numberFrameLost = ' + str(lastPoint.numberLostFrame) + ' minDis = ' + str(lastPoint.tempMinDistance)
                        obj = Object(tempLastPoint.tempNextPoint[X], tempLastPoint.tempNextPoint[Y], rad, True)
                        self.allObj.append(obj)


    def isAllOldPointMapped(self):
        count = 0
        for ob in self.allObj:
            if isinstance(ob,Object):
                if not ob.isExist:
                    count += 1
        return count == 0