__author__ = 'anhdt'
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
import tracking
import detect
LINE_POS_TOP, LINE_POS_BOT = [144-50, 144+50]
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
            tracking.resetTracking()

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
                    ck, data = detect.checkPeople(display,ponto1,ponto2,xindex)
                    if ck:
                        for datax in data:
                            pon1 = (ponto1[0]+datax[0][0],ponto1[1]+datax[0][1])
                            pon2 = (pon1[0]+datax[1][0]-datax[0][0],ponto1[1]+datax[1][1])
                            # cv2.rectangle(display, pon1, pon2,(255,255,255), 2)
                    if locRec(ponto1,ponto2):
                        cv2.rectangle(display,ponto1, ponto2,(255,255,255), 2)
                        tracking.check_nextline(ponto1,ponto3)
            tracking.remove_track()
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