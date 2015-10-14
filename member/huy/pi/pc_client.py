import numpy
import sys
import threading
import cv2

__author__ = 'huybu'


class PCClient(threading.Thread):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]

    def __init__(self, addr, capture_right, capture_left, udpSocket):
        super(PCClient, self).__init__()
        self.addr = addr
        self.running = True
        self.capture_right = capture_right
        self.capture_left = capture_left
        self.udpSocket = udpSocket

    def run(self):
        while self.running:
            try:
                ret, frameRight = self.capture_right.read()
                ret, frameLeft = self.capture_left.read()
                comRight = numpy.array(cv2.imencode('.jpg', frameRight, self.encode_param)[1]).tostring()
                comLeft = numpy.array(cv2.imencode('.jpg', frameLeft, self.encode_param)[1]).tostring()
                dataRight = numpy.array(comRight)
                dataLeft = numpy.array(comLeft)
                stringData = dataRight.tostring() + "daicahuy" + dataLeft.tostring()
                self.udpSocket.sendto(stringData, self.addr)
            except Exception, ex:
                print str(ex)
                self.stopThread()
                pass

    def stopThread(self):
        self.running = False
