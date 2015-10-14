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
        data = numpy.fromstring(reply, dtype='uint8')
        decimg=cv2.imdecode(data,1)
        cv2.imshow('SERVER'+str(count),decimg)
        cv2.waitKey(50)


    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()