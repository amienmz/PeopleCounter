from stereovision.calibration import StereoCalibration
import cv2
import numpy as np
import cv2
import numpy
import time
import zlib
import const
import socket  # for sockets
import sys  # for exit
#==================================================#
#====================Detect========================#
#==================================================#

WIDTH_PCONS, HEIGHT_PCONS = [100,100]
WIDTH_HCONS, HEIGHT_HCONS = [50,50]
SIZE_HEAD_MAX, SIZE_HEAD_MIN = [1.08,0.3]
HEIGHT_IMG, WIDTH_IMG = [288,352]
LINE_POS_TOP, LINE_POS_BOT = [144-50, 144+50]

def checkHead(img,pon1,pon2):
    if pon2[1] - pon1[1] < WIDTH_HCONS or pon2[0] - pon1[0] < WIDTH_HCONS:
        return False
    else:
        return True
    # if SIZE_HEAD_MIN < (pon2[1]*1.0)/(pon2[0]*1.0) < SIZE_HEAD_MAX:
    #     return True
    # else:
    #     return False

def checkHumanWithHead(data,w_b,h_b):
    nhyHead = len(data)
    if nhyHead == 1:
        lfx=data[0][0][0]
        rgx=w_b-data[0][1][0]-lfx
        if rgx < data[0][1][0] and lfx < data[0][1][0]:
            return True
        else:
            return False
    elif nhyHead > 1:
        return True
    else:
        return False

def checkPeople(img,pon1,pon2,xindex):
    if pon2[1] - pon1[1] < WIDTH_PCONS or pon2[0] - pon1[0] < HEIGHT_PCONS:
        return False , None
    imgx = img[pon1[1]:pon2[1],pon1[0]:pon2[0]]
    wx,hx = imgx.shape
    ret, data = cv2.threshold(imgx,imgx.mean()+40,imgx.max(),cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(data,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    datax = []
    for cn in contours:
        ver = cv2.boundingRect(cn)
        if cv2.contourArea(cn) > 300:
            maiorArea = cv2.contourArea(cn)
            rect = ver
            # print rect
            ponto1 = (rect[0], rect[1])
            ponto2 = (rect[0]+ rect[2],rect[1]+rect[3])
            if checkHead(imgx,ponto1,ponto2):
                datax.append([ponto1,ponto2])
            # ponx1 = (pon1[0]+ponto1[0],pon1[1]+ponto1[1])
            # ponx2 = (ponx1[0]+ponto2[0]-ponto1[0],pon1[1]+ponto2[1])
            # cv2.rectangle(img, ponx1, ponx2,(255,255,255), 2)
    # checkHumanWithHead(datax,pon2[0],pon2[1])
    # cv2.imshow("xxx %i"%xindex,imgx)
    # cv2.imshow("xxx %i"%xindex,imgx)
    if checkHumanWithHead(datax,wx,hx):
        # cv2.imshow("xxx %i"%xindex,imgx)
        return True , datax
    else:
        return False, None
    # return False, None

def locRec(pon1,pon2):
    if pon2[1] - pon1[1] < WIDTH_HCONS or pon2[0] - pon1[0] < WIDTH_HCONS:
        return False
    else:
        return True

#==================================================#
#===================End Detect=====================#
#==================================================#

def nothing(x):
    pass
#
# video1 = cv2.VideoCapture('../../Datas/outputR24.avi') #right
# video1.set(3,352)
# video1.set(4,288)
#
# video2 = cv2.VideoCapture('../../Datas/outputL24.avi')
# video2.set(3,352)
# video2.set(4,288)

# This assumes you've already calibrated your camera and have saved the
# calibration files to disk. You can also initialize an empty calibration and
# calculate the calibration, or you can clone another calibration from one in
# memory
calibration = StereoCalibration(input_folder='../../Datas/data')

minDisparity = 8
numDisparities = 3 *16
SADWindowSize = 1 #old number
P1 = 35
P2 = 89
disp12MaxDiff = 0
preFilterCap = 0
uniquenessRatio = 0
speckleWindowSize = 0
speckleRange = 0
fullDP = True
block_matcher = cv2.StereoSGBM(minDisparity, numDisparities, SADWindowSize, P1, P2,disp12MaxDiff,preFilterCap, uniquenessRatio, speckleWindowSize,speckleRange,fullDP)
fgbg = cv2.BackgroundSubtractorMOG2(history=10, varThreshold=100, bShadowDetection=1)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
#======================================#
#==============Tracking================#
#======================================#
allObj = []
InSh = 0
OutSh = 0
def resetTracking():
    for data in allObj:
        data[4] = False
    return None

def remove_track():
    for data in allObj:
        if data[4] == False:
            data[0] = None
            data[1] = None
            data[2] = None
            data[3] = None
            data[5] = 0
            data[6] = 0
    return None

def check_in_out(data):
    #0: out
    #1: in
    #-1: unknow
    if data[5] > 0  and data[6] > 0:
        if data[5] >  data[6]:
            data[5] = 0
            data[6] = 0
            return 1
        else:
            data[5] = 0
            data[6] = 0
            return 0
    else:
        return -1
def sysn_line(data,y,h):
    ln = check_withLine(y,h)
    if ln < 0:
        return False
    if data[5] == 0 or data[5] == ln:
        data[5] = ln
    elif data[6] == 0 or data[6] == ln:
        data[6] = ln
    return True
def check_withLine(y,h):
    if y <= LINE_POS_TOP <= y+h:
        return 1
    elif y <= LINE_POS_BOT <= y+h:
        return 2
    else:
        return -1

def check_nextline(pon1,pon2):
    global InSh , OutSh
    y, x = [pon1[1],pon1[0]]
    h, w = [pon2[1],pon2[0]]
    # print x,y,w,h
    if len(allObj) == 0:
        allObj.append([x,y,w,h,True,0,0])
        return None
    haveline = False
    for data in allObj:
        if data[0] != None:
            if (data[1] <= y <= data[1]+data[3] and x <= data[0] <= x + w) or (x<=data[0]<=x+w and y <= data[1]<=y+h)or (data[0] <= x <= data[0] + data[2] and y<=data[1]<=y+h) or (data[0] <= x <= data[0]+data[2] and data[1]<=y<=data[1]+data[3]):
                # Point1 = ((data[0]+data[2])/2,(data[1]+data[3])/2)
                data[0] = x
                data[1] = y
                data[2] = w
                data[3] = h
                data[4] = True
                if sysn_line(data,y,h) == False:
                    inout = check_in_out(data)
                    if inout == 0:
                        OutSh +=1
                    elif inout == 1:
                        InSh +=1
                # Point2 = ((data[0]+data[2])/2,(data[1]+data[3])/2)
                # cv2.line(img,Point1,Point2,(255,255,255),1)
                # ins = allObj.index(data)
                # allObj.insert(ins,[x,y,w,h,True])
                # allObj.remove(x)
                haveline = True
                break
    if haveline == False:
        try:
            ins = allObj.index([None,None,None,None,False,0,0])
            allObj.insert(ins,[x,y,w,h,True,0,0])
            allObj.remove(allObj[ins+1])
        except Exception as e:
            allObj.append([x,y,w,h,True,0,0])
    return None


#======================================#
#============End Tracking==============#
#======================================#

# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

# HOST = '10.20.13.171';
HOST = 'localhost';
PORT = 8888;

count = 0

try:
    # Set the whole string
    s.sendto(const.CMD_CONNECT, (HOST, PORT))

    # receive data from client (data, addr)
    first = None

    font = cv2.FONT_HERSHEY_SIMPLEX

    while True:
        try:
            char = cv2.waitKey(10)
            d = s.recvfrom(50000)
            count += 1
            if count == 1:
                first = time.time()
            reply = zlib.decompress(d[0])
            # reply = d[0]
            addr = d[1]
            arr = reply.split('daicahuy')
            dataRight = numpy.fromstring(arr[0], dtype='uint8')
            dataLeft = numpy.fromstring(arr[1], dtype='uint8')
            decimgRight = cv2.imdecode(dataRight, 1)
            decimgLeft = cv2.imdecode(dataLeft, 1)

            imgR = cv2.cvtColor(decimgRight,cv2.COLOR_RGB2GRAY)
            imgL = cv2.cvtColor(decimgLeft,cv2.COLOR_RGB2GRAY)

            rectified_pair = calibration.rectify((imgL, imgR))

            disparity = block_matcher.compute(rectified_pair[0], rectified_pair[1])

            display = cv2.normalize(disparity,disparity, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

            # cv2.imshow("Before filter", display)
            if (char == 100):
                cv2.imwrite("test.jpg",display)
            display = display[20:288,20:335]

            opening = cv2.morphologyEx(display,cv2.MORPH_OPEN,kernel, iterations = 3)
            re,thresh1 = cv2.threshold(opening,75,255,cv2.THRESH_BINARY)
            sure_bg = cv2.dilate(thresh1,kernel,iterations=3)
            cinza = cv2.erode(sure_bg,kernel,iterations = 3)
            contours, hierarchy = cv2.findContours(cinza,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            xindex = 0
            # cv2.imshow("mask", thresh1)
            resetTracking()

            for cn in contours:
                ver = cv2.boundingRect(cn)
                if cv2.contourArea(cn) > 500:
                    maiorArea = cv2.contourArea(cn)
                    rect = ver
                    # print rect
                    xindex += 1
                    ponto1 = (rect[0], rect[1])
                    ponto2 = (rect[0]+ rect[2],rect[1]+rect[3])
                    ponto3 = (rect[2],rect[3])
                    ck, data = checkPeople(display,ponto1,ponto2,xindex)
                    if ck:
                        for datax in data:
                            pon1 = (ponto1[0]+datax[0][0],ponto1[1]+datax[0][1])
                            pon2 = (pon1[0]+datax[1][0]-datax[0][0],ponto1[1]+datax[1][1])
                            # cv2.rectangle(display, pon1, pon2,(255,255,255), 2)
                    if locRec(ponto1,ponto2):
                        cv2.rectangle(display,ponto1, ponto2,(255,255,255), 2)
                        check_nextline(ponto1,ponto3)
            remove_track()
            # print allObj
            cv2.line(display,(0,LINE_POS_TOP),(352,LINE_POS_TOP),(255,255,255),1)
            cv2.line(display,(0,LINE_POS_BOT),(352,LINE_POS_BOT),(255,255,255),1)
            cv2.putText(display,'In: %i'%InSh,(50,220), font, 0.5,(255,255,255),1)
            cv2.putText(display,'Out: %i'%OutSh,(200,220), font, 0.5,(255,255,255),1)
            cv2.imshow("res",display)
            # char = cv2.waitKey(10)
            if (char == 99):
                cv2.waitKey(0)

            if (char == 27):
                break
            duration = (time.time() - first)
            print " pp: " + str(count / duration) + " p/s" + " duration = " + str(duration)

        except Exception, ex:
            print 'Unwanted exception: ' + str(ex)
            pass

except socket.error, msg:
    print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()


cv2.destroyAllWindows()