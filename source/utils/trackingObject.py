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
            data.clearTemp()
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

        # print x,y,w,h
        haveline = False
        if len(self.allObj) == 0:
            for newPoint in arrPointObject:
                obj = Object(newPoint[X], newPoint[Y], rad, True)
                self.allObj.append(obj)
                return

        # # sort listobject by noNumberLostFrame
        # self.allObj.sort(key=lambda x: x.numberLostFrame, reverse=False)

        # newpoint - is map with last point
        dictNewPointMapped = {}
        # print '1'
        for newPoint in arrPointObject:
            dictNewPointMapped.update({str(newPoint): False})
            # print '2'
            minLength = 9999
            tempPoint = None
            for lastPoint in self.allObj:
                if isinstance(lastPoint, Object):
                    lenth = lastPoint.calculatorDistanceToPoint(newPoint)
                    if lenth < minLength:
                        minLength = lenth
                        tempPoint = lastPoint
            if tempPoint is None:
                continue
            if tempPoint.tempNextPoint is None:
                tempPoint.tempMinDistance = minLength
                tempPoint.tempNextPoint = newPoint
                dictNewPointMapped.update({str(newPoint): True})
                # print '3'
            elif tempPoint.tempMinDistance < minLength:
                # edit last map point to false
                dictNewPointMapped.update({str(tempPoint.tempNextPoint): False})
                # print '4'
                tempPoint.tempMinDistance = minLength
                tempPoint.tempNextPoint = newPoint
                dictNewPointMapped.update({str(newPoint): True})
                # print '5'

        for newPoint in arrPointObject:
            if not dictNewPointMapped.has_key(str(newPoint)):
                obj = Object(newPoint[X], newPoint[Y], rad, True)
                self.allObj.append(obj)
            elif not dictNewPointMapped[str(newPoint)]:
                obj = Object(newPoint[X], newPoint[Y], rad, True)
                self.allObj.append(obj)
        # print '6'
        for lastPoint in self.allObj:
            if isinstance(lastPoint, Object):
                if not lastPoint.tempNextPoint is None:
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
                    lastPoint.AddFramePass()
