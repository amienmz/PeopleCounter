import multiprocessing
from multiprocessing.dummy import current_process
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

class Stream_Process(multiprocessing.Process):
    def __init__(self, mac):
        multiprocessing.Process.__init__(self)
        self.macid = mac
        # Datagram (udp) socket
        try:
            self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print 'Socket created'
        except socket.error, msg:
            print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            return

        # try:
        #     os.system("killall -9 Stream_Process")
        # except socket.error, msg:
        #     print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        # Bind socket to local host and port

        # now keep talking with the client
        self.capture_right = None
        self.capture_left = None
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
        self.client = None

    def stop_client_thread(self):
        try:
            if self.client is not None:
                self.client.stopthread()
                time.sleep(0.1)
                self.client.join()
            time.sleep(0.1)
        except Exception, ex:
            print 'Unwanted exception stop_client_thread: ' + str(ex)
        try:
            self.client = None
        except:
            pass
        time.sleep(0.1)

    def run(self):
        try:
            self.udpSocket.bind(('', const.PORT))
        except socket.error, msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            try:
                os.kill(os.getpid(),9)
                print('kill OK')
            except:
                print 'can not self kill PROCESS'
                return


        print 'Socket bind complete'

        while True:
            try:
                print 'check'
                # receive data from client (data, addr)
                datagram = self.udpSocket.recvfrom(1024)
                data = datagram[const.POS_DATA]
                address = datagram[const.POS_ADDRESS]
                print "connect from " + address[const.POS_IP]
                if data == const.CMD_CONNECT:
                    self.stop_client_thread()
                    capture_right = cv2.VideoCapture(0)
                    capture_right.set(3, 352)
                    capture_right.set(4, 288)
                    capture_right.set(5, 24)
                    capture_left = cv2.VideoCapture(1)
                    capture_left.set(3, 352)
                    capture_left.set(4, 288)
                    capture_left.set(5, 24)
                    self.client = PCClient(address, capture_right, capture_left, self.udpSocket)
                    self.client.start()
                if data == const.CMD_CHECK:
                    self.udpSocket.sendto(MAC_ADD, (address[const.POS_IP],9999))
                if data == const.CMD_DISCONNECT:
                    self.stop_client_thread()
            except KeyboardInterrupt:
                print 'Interrupted catched'
                try:
                    if self.client is not None:
                        self.client.stopthread()
                    self.udpSocket.close()
                    cv2.destroyAllWindows()
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)
            except Exception, ex:
                print 'Unwanted exception: ' + str(ex)
                self.stop_client_thread()
                pass

        try:
            self.udpSocket.close()
            cv2.destroyAllWindows()
        except:
            print('close udp exception')
            pass

        try:
            os.kill(os.getpid(),9)
            print('kill OK')
        except:
            print 'can not self kill PROCESS'
            pass

if __name__ == "__main__":
    MAC_ADD = ''
    try:
        mac = get_mac()
        MAC_ADD = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
    except:
        pass
    try:
        stream_process = Stream_Process(mac)
        stream_process.start()
    except:
        pass

    while True:
        time.sleep(2)
        try:
            print 'alive = ' + str(stream_process.is_alive())
            if not stream_process.is_alive():
                stream_process = Stream_Process(mac)
                stream_process.start()
                time.sleep(1)
        except Exception, ex:
                print 'WHILE SLEEP 2s EXCEPTION ' + str(ex)
                pass


