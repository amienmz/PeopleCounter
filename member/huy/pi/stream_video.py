import cv2
import numpy

__author__ = 'huybu'

import socket
import sys
import pc_client
import const
from thread import start_new_thread

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

lst_conn = []

# Datagram (udp) socket
try :
    udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

# Bind socket to local host and port
try:
    udpSocket.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

def client_thread(conn):
    conn.send("Welcome to the Server. Type messages and press enter to send.\n")

    while True:
        data = conn.recv(1024)
        if not data:
            break
        reply = "OK . . " + data
        conn.sendall(reply)
    conn.close()

#now keep talking with the client
capture = cv2.VideoCapture(0)
capture.set(3,352)
capture.set(4,288)
encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),40]
while True:
    # receive data from client (data, addr)
    datagram = udpSocket.recvfrom(1024)
    data = datagram[const.POS_DATA]
    addr = datagram[const.POS_ADDRESS]
    if data == const.CMD_CONNECT:
        # lst_conn.append(pc_client(addr,udpSocket))

        # while True:
        ret, frame = capture.read()
        com = numpy.array(cv2.imencode('.jpg', frame)[1]).tostring()
        data = numpy.array(com)
        stringData = data.tostring()
        udpSocket.sendto(stringData,addr)

udpSocket.close()