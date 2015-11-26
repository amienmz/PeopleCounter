__author__ = 'pc'
import cv2
import numpy as np

class TrackingObj(object):
    def __init__(self):
        self.allObj = []
        self.InSh = 0
        self.OutSh = 0
        self.maxPass = 10
        self.topPosition = 144-70
        self.midPosition = 144
        self.botPosition = 144+70


    def resetTracking(self):
        for data in self.allObj:
            data[4] = False
        return None

    def remove_track(self):
        for data in self.allObj:
            if data[4] == False:
                if data[6] < self.maxPass:
                    data[6] += 1
                else:
                    self.allObj.remove(data)
                    # data[0] = None
                    # data[1] = None
                    # data[2] = None
                    # data[3] = None
                    # data[5] = 0
                    # data[6] = 0
        return None

    def check_in_out(self,data,ln):
        #0: out
        #1: in
        #-1: unknow
        if data[5] > 0 and ln != None:
            data[5] = 0
            if ln == 0:
                return 1
            else:
                return 0
        else:
            return -1

    def sysn_line(self,data,y,h):
        ln = self.check_withLine(y,h)
        if ln == 1:
            data[5] = ln
            return False,ln
        else:
            return True,ln


    def check_withLine(self,y,h):
        if y <= self.topPosition <= y+h:
            return 0

        elif y <= self.botPosition <= y+h:
            return 2

        elif y <= self.midPosition <= y+h:
            return 1


    def check_Obj(self,pon1,pon2):
        y, x = [pon1[1],pon1[0]]
        h, w = [pon2[1],pon2[0]]
        if len(self.allObj) == 0:
            return False
        haveline = False
        for data in self.allObj:
            if data[0] != None:
                if (data[1] <= y <= data[1]+data[3] and x <= data[0] <= x + w) or (x<=data[0]<=x+w and y <= data[1]<=y+h)or (data[0] <= x <= data[0] + data[2] and y<=data[1]<=y+h) or (data[0] <= x <= data[0]+data[2] and data[1]<=y<=data[1]+data[3]):
                    # Point1 = ((data[0]+data[2])/2,(data[1]+data[3])/2)
                    data[0] = x
                    data[1] = y
                    data[2] = w
                    data[3] = h
                    data[4] = True
                    res, ln = self.sysn_line(data,y,h)
                    if res:
                        inout = self.check_in_out(data,ln)
                        if inout == 0:
                            self.OutSh +=1
                        elif inout == 1:
                            self.InSh +=1
                    haveline = True
                    break
        if haveline == False:
            return False
        return True

    def trackingObj(self,pon1,pon2):
        y, x = [pon1[1],pon1[0]]
        h, w = [pon2[1],pon2[0]]
        # print x,y,w,h
        if len(self.allObj) == 0:
            self.allObj.append([x,y,w,h,True,0,0])
            return None
        haveline = False
        for data in self.allObj:
            if data[0] != None:
                if (data[1] <= y <= data[1]+data[3] and x <= data[0] <= x + w) or (x<=data[0]<=x+w and y <= data[1]<=y+h)or (data[0] <= x <= data[0] + data[2] and y<=data[1]<=y+h) or (data[0] <= x <= data[0]+data[2] and data[1]<=y<=data[1]+data[3]):
                    # Point1 = ((data[0]+data[2])/2,(data[1]+data[3])/2)
                    data[0] = x
                    data[1] = y
                    data[2] = w
                    data[3] = h
                    data[4] = True
                    res, ln = self.sysn_line(data,y,h)
                    if res:
                        inout = self.check_in_out(data,ln)
                        if inout == 0:
                            self.OutSh +=1
                        elif inout == 1:
                            self.InSh +=1
                    haveline = True
                    break
        if haveline == False:
            try:
                ins = self.allObj.index([None,None,None,None,False,0,0])
                self.allObj.insert(ins,[x,y,w,h,True,0,0])
                self.allObj.remove(self.allObj[ins+1])
            except Exception as e:
                self.allObj.append([x,y,w,h,True,0,0])
        return None


