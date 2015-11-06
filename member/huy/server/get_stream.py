import cv2
import numpy
import time
import zlib
import const
import socket  # for sockets
import sys  # for exit

__author__ = 'huybu'

# create dgram udp socket
try:
    pi_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

# HOST = '10.20.13.171';
HOST = 'localhost';
PORT = 8888;

count = 0

try:
    # Set the whole string
    pi_socket.sendto(const.CMD_CONNECT, (HOST, PORT))

    # receive data from client (data, addr)
    first = None
    while True:
        # try:

            d = pi_socket.recvfrom(50000)
            count += 1
            if count == 1:
                first = time.time()
            reply = (d[0])
            # reply = d[0]
            addr = d[1]
            arr = reply.split('daicahuy')
            dataRight = numpy.fromstring(arr[0], dtype='uint8')
            dataLeft = numpy.fromstring(arr[1], dtype='uint8')
            decimgRight = cv2.imdecode(dataRight, 1)
            decimgLeft = cv2.imdecode(dataLeft, 1)
            # cv2.imshow('SERVER RIGHT', decimgRight)
            # cv2.imshow('SERVER LEFT', decimgLeft)
            duration = (time.time() - first)
            print " pp: " + str(count / duration) + " p/s" + " duration = " + str(duration)
            cv2.waitKey(1)
        # except:
        #     print 'Exception: ' + sys.exc_info()[0]
        #     pass


except socket.error, msg:
    print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
