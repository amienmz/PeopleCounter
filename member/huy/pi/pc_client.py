import socket
import numpy
import sys
import threading
import cv2
import time
import zlib
__author__ = 'huybu'


class PCClient(threading.Thread):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]

    def __init__(self, addr, capture_right, capture_left, udpSocket):
        super(PCClient, self).__init__()
        self.address = addr
        self.running = True
        self.capture_right = capture_right
        self.capture_left = capture_left
        self.udpSocket = udpSocket

    def run(self):
        while self.running:
            try:
                ret, frame_right = self.capture_right.read()
                ret, frame_left = self.capture_left.read()
                # comRight = numpy.array(cv2.imencode('.jpg', frame_right, self.encode_param)[1]).tostring()
                # comLeft = numpy.array(cv2.imencode('.jpg', frame_left, self.encode_param)[1]).tostring()
                # dataRight = numpy.array(comRight)
                # dataLeft = numpy.array(comLeft)
                dataRight = numpy.array(cv2.imencode('.jpg', frame_right, self.encode_param)[1])
                dataLeft = numpy.array(cv2.imencode('.jpg', frame_left, self.encode_param)[1])
                stringData = dataRight.tostring() + "daicahuy" + dataLeft.tostring()
                self.udpSocket.sendto(stringData, self.address)
                time.sleep(0.05)
            except Exception, ex:
                print 'stop client exception'
                print str(ex)
                self.stopthread()
                break

    def stopthread(self):
        print 'stop client'
        try:
            self.capture_right.release()
            self.capture_left.release()
        except:
            pass
        self.running = False
