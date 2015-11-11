import threading
import cv2
import time
from member.huy.server.gui.frm_camera import FrmCamera
import socket
import multiprocessing
import sys
import numpy
from source.utils import const


class PC_Manager(object):
    def __init__(self,ip_address,root_tk,lock):
        self.ip_address = ip_address
        self.queue_process_to_frm = multiprocessing.Queue()
        self.queue_thread_to_process = multiprocessing.Queue()
        self.root = root_tk
        self.frm_camera = FrmCamera(self.root, lock,self.queue_process_to_frm)
        self.lock = lock
        # create process
        self.process_pc = Process_People_Counter(self.ip_address,self.queue_process_to_frm)

    def start(self):
        self.process_pc.start()
        self.frm_camera.toplevel.after(0, func=lambda: self.frm_camera.update_video())

class Process_People_Counter(multiprocessing.Process):
    def __init__(self, ip_address,queue_process_to_frm):
        multiprocessing.Process.__init__(self)
        self.ip_address = ip_address
        self.queue_process_to_frm = queue_process_to_frm
        self.running = True

    def run(self):
        print "I'm here " + self.ip_address
        # create dgram udp socket
        try:
            self.pi_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error:
            print 'Failed to create socket'
            return
        try:
            # Set the whole string
            self.pi_socket.sendto(const.CMD_CONNECT, (self.ip_address, const.PORT))
            print 'send ok'
            while self.running:
                try:
                    t1 = time.time()
                    reply, addr = self.pi_socket.recvfrom(50000)
                    arr = reply.split('daicahuy')
                    dataRight = numpy.fromstring(arr[0], dtype='uint8')
                    dataLeft = numpy.fromstring(arr[1], dtype='uint8')
                    decimgRight = cv2.imdecode(dataRight, 1)
                    decimgLeft = cv2.imdecode(dataLeft, 1)
                    self.queue_process_to_frm.put(decimgRight)
                    cv2.waitKey(1)
                    print 'fps = ' + str(1/(time.time()-t1))
                except Exception, ex:
                    print 'Thread_Listening_Socket Exception: ' + str(ex)

        except Exception, ex:
            print 'Thread_Listening_Socket Exception: ' + str(ex)
        # cap = cv2.VideoCapture(int(self.ip_address))
        # while True:
        #     try:
        #         ret,frame = cap.read()
        #         self.queue_process_to_frm.put(frame)
        #         cv2.waitKey(1)
        #     except Exception, ex:
        #         print 'thread_camera Exception: ' + str(ex)
