import threading
import cv2
from member.huy.server.gui.frm_camera import FrmCamera

__author__ = 'huybu'
import multiprocessing
import sys
import re

class Streamer(object):
    def __init__(self,ip_address,root_tk,lock):
        self.ip_address = ip_address
        self.queue = multiprocessing.Queue()
        self.root = root_tk
        self.frm_camera = FrmCamera(self.root, lock)
        self.lock = lock
        # create process
        self.process_streamer = Process_Streamer(self.ip_address,self.queue)

    def start(self):
        self.process_streamer.start()
        self.frm_camera.toplevel.after(0, func=lambda: self.frm_camera.update_video(self.queue))

# class Thread_Camera(threading.Thread):
#     def __init__(self,ip_address, root_tk, frm_camera,lock):
#         self.ip_address = ip_address
#         self.root = root_tk
#         self.frm_camera = frm_camera
#         self.running=True
#         self.lock = lock
#     def run(self):
#         while self.running:
#             try:
#                 self.lock.acquire()
#                 ret,frame = cap.read()
#                 self.root.after(0, func=lambda: self.lst_frm_camera[index].update_video(frame))
#                 # self.frm_camera.update_video(frame)
#                 cv2.waitKey(1)
#             except Exception, ex:
#                 print 'thread_camera Exception: ' + str(ex)
#             finally:
#                 self.lock.release()
#     def stop_thread(self):
#         self.running=False

class Process_Streamer(multiprocessing.Process):
    def __init__(self, ip_address,queue):
        multiprocessing.Process.__init__(self)
        self.ip_address = ip_address
        self.queue = queue

    def run(self):
        print "I'm here " + self.ip_address
        cap = cv2.VideoCapture(int(self.ip_address))
        while True:
            try:
                ret,frame = cap.read()
                self.queue.put(frame)
                cv2.waitKey(1)
            except Exception, ex:
                print 'thread_camera Exception: ' + str(ex)
