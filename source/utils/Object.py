__author__ = 'pc'
import math
X = 0
Y = 1
class Object(object):
    def __init__(self,x,y,radius,isExist, color):
        self.x = x
        self.y = y
        self.r = radius
        self.isExist = isExist
        self.center = False
        self.numberLostFrame = 0
        self.linepass = None
        self.tempMinDistance = 9999
        self.tempNextPoint = None
        self.historyPoints = [(x,y)]
        self.color = color

    def calculatorDistanceToPoint(self,point):
        # return math.sqrt(math.pow(2,self.x-point[X])+math.pow(2,self.y-point[Y]))
        return math.hypot(point[X] - self.x, point[Y] - self.y)

    def clearTemp(self):
        self.tempMinDistance=9999
        self.tempNextPoint = None


    def updateObject(self):
        self.x = self.tempNextPoint[X]
        self.y = self.tempNextPoint[Y]
        self.historyPoints.append((self.x,self.y))
        self.isExist = True
        self.numberLostFrame = 0

    def UpdateTracking(self,x,y):
        self.historyPoints.append((x,y))
        self.x = x
        self.y = y
        self.isExist = True
        self.numberLostFrame = 0

    def ClearExist(self):
        self.isExist = False

    def AddFramePass(self):
        self.numberLostFrame += 1

    def InLineCenter(self):
        self.center = True

    def UpdateLinePass(self,ln):
        if (self.center == False) and ln!= None and (ln != self.linepass):
            self.linepass = ln
            return True
        else:
            return False

    def CheckObject(self,x,y):
        if (abs(x-self.x)<self.r*2 and abs(y-self.y)<self.r*2):
            return True
        else:
            return False

    def CheckInOut(self,ln):
        #0: out
        #1: in
        #-1: unknow
        if self.center and ln!=None and ln != self.linepass:
            self.linepass = ln
            self.center = False
            if ln == 0:
                return 1
            else:
                return 0
        else:
            return -1

    def displayDebug(self):
        print self.x,self.y,self.isExist,self.numberLostFrame,self.linepass,self.center