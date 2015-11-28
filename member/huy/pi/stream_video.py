import os
import cv2
import numpy
import time
import zlib

__author__ = 'huybu'

import socket
import sys
from pc_client import PCClient
import const
from uuid import getnode as get_mac


MAC_ADD = ''
HOST = ''  # Symbolic name meaning all available interfaces
PORT = 8888  # Arbitrary non-privileged port
try:
    mac = get_mac()
    MAC_ADD = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
except:
    pass
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
capture_right = None
capture_left = None
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
client = None


def stop_client_thread():
    global client
    try:
        if client is not None:
            client.stopthread()
            time.sleep(0.1)
            client.join()
        time.sleep(0.1)
    except Exception, ex:
        print 'Unwanted exception stop_client_thread: ' + str(ex)
    try:
        client = None
    except:
        pass
    time.sleep(0.1)


while True:
    try:
        print 'check'
        # receive data from client (data, addr)
        datagram = udpSocket.recvfrom(1024)
        data = datagram[const.POS_DATA]
        address = datagram[const.POS_ADDRESS]
        print "connect from " + address[const.POS_IP]
        if data == const.CMD_CONNECT:
            stop_client_thread()
            capture_right = cv2.VideoCapture('../../../data/outputR24.avi')
            capture_right.set(3, 352)
            capture_right.set(4, 288)
            capture_right.set(5, 24)
            capture_left = cv2.VideoCapture('../../../data/outputL24.avi')
            capture_left.set(3, 352)
            capture_left.set(4, 288)
            capture_left.set(5, 24)
            client = PCClient(address, capture_right, capture_left, udpSocket)
            client.start()
        if data == const.CMD_CHECK:
            udpSocket.sendto(MAC_ADD, (address[const.POS_IP],9999))
        if data == const.CMD_DISCONNECT:
            stop_client_thread()
    except KeyboardInterrupt:
        print 'Interrupted catched'
        try:
            if client is not None:
                client.stopthread()
            udpSocket.close()
            cv2.destroyAllWindows()
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    except Exception, ex:
        print 'Unwanted exception: ' + str(ex)
        stop_client_thread()
        pass

udpSocket.close()
cv2.destroyAllWindows()
