import cv2
import numpy

__author__ = 'huybu'

import socket
import sys
from pc_client import PCClient
import const
from thread import start_new_thread

HOST = ''  # Symbolic name meaning all available interfaces
PORT = 8888  # Arbitrary non-privileged port

lst_conn = []

# Datagram (udp) socket
try:
    udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg:
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

# Bind socket to local host and port
try:
    udpSocket.bind((HOST, PORT))
except socket.error, msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'


# now keep talking with the client
# capture_right = cv2.VideoCapture(0)
# capture_right.set(3,352)
# capture_right.set(4,288)
# capture_left = cv2.VideoCapture(1)
# capture_left.set(3,352)
# capture_left.set(4,288)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
while True:
    try:
        print 'check'
        # receive data from client (data, addr)
        datagram = udpSocket.recvfrom(1024)
        data = datagram[const.POS_DATA]
        address = datagram[const.POS_ADDRESS]
        if data == const.CMD_CONNECT:
            capture_right = cv2.VideoCapture(0)
            capture_right.set(3, 352)
            capture_right.set(4, 288)
            capture_left = cv2.VideoCapture(1)
            capture_left.set(3, 352)
            capture_left.set(4, 288)
            client = PCClient(address,capture_right,capture_left,udpSocket)
            # lst_conn.append(client)
            client.start()
            # while True:
            #     ret, frameRight = capture_right.read()
            #     ret, frameLeft = capture_right.read()
            #     comRight = numpy.array(cv2.imencode('.jpg', frameRight, encode_param)[1]).tostring()
            #     comLeft = numpy.array(cv2.imencode('.jpg', frameLeft, encode_param)[1]).tostring()
            #     dataRight = numpy.array(comRight)
            #     dataLeft = numpy.array(comLeft)
            #     stringData = dataRight.tostring() + "daicahuy" + dataLeft.tostring()
            #     udpSocket.sendto(stringData, addr)
            #     cv2.waitKey(10)
    except Exception, ex:
        print str(ex)
        pass

udpSocket.close()
# capture_right.release()
# capture_left.release()
cv2.destroyAllWindows()
