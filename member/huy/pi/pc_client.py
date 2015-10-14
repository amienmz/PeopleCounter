import numpy

__author__ = 'huybu'
import threading
import cv2


class PCClient (threading.Thread):
    def __init__(self,addr,udpSocket):
        self.addr = addr
        self.running = True
        self.udpSocket = udpSocket
    def run(self):
        capture = cv2.VideoCapture(0)
        capture.set(3,352)
        capture.set(4,288)
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),40]

        while self.running:
            ret, frame = capture.read()
            result, imgencode = cv2.imencode('.jpg', frame, encode_param)
            data = numpy.array(imgencode)
            stringData = data.tostring()
            self.udpSocket.sendto(stringData,self.addr)
            # do something

            break
    classmethod
    def stopThread(self):
        self.running=False