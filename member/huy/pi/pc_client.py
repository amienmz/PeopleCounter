import socket
import numpy
import sys
import threading
import cv2
import time
import zlib
from datetime import datetime
import const
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

    def log(self, mess):
        try:
            with open("log.txt", "a") as myfile:
                myfile.write(str(datetime.now())+": "+mess+"\r\n")
        except:
            pass

    def run(self):
        count_dead = 0
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
                stringData = dataRight.tostring() + const.JOIN + dataLeft.tostring()
                self.udpSocket.sendto(stringData, self.address)
                count_dead = 0
            except Exception, ex:
                count_dead += 1
                print 'Exception PCClient.run ' + str(ex)
                self.log('Exception PCClient.run ' + str(ex))
                if count_dead == 20:
                    self.stopthread()
                break

    def stopthread(self):
        print 'PCClient.stopclient'
        self.log('PCClient.stopclient')
        try:
            self.capture_right.release()
            self.capture_left.release()
        except Exception, ex:
            print 'Exception PCClient.stopthread ' + str(ex)
            self.log('Exception PCClient.stopthread ' + str(ex))
            pass
        self.running = False
