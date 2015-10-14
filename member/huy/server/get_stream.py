import cv2
import numpy
import time

__author__ = 'huybu'
'''
    udp socket client
    Silver Moon
'''

import socket   #for sockets
import sys  #for exit

# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

# host = '10.20.13.171';
host = 'localhost';
port = 8888;


while True:
    try :
        #Set the whole string
        s.sendto('connect', (host, port))


        # receive data from client (data, addr)
        count=0
        # while True:
        d = s.recvfrom(60000)
        reply = d[0]
        addr = d[1]
        arr = reply.split('daicahuy')
        dataRight = numpy.fromstring(arr[0], dtype='uint8')
        dataLeft = numpy.fromstring(arr[1], dtype='uint8')
        decimgRight=cv2.imdecode(dataRight,1)
        decimgLeft=cv2.imdecode(dataLeft,1)
        cv2.imshow('SERVER RIGHT'+str(count),decimgRight)
        cv2.imshow('SERVER LEFT'+str(count),decimgLeft)
        cv2.waitKey(50)


    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()