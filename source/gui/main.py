import Queue
from multiprocessing import Process
import multiprocessing
import os
import threading
import cv2
# from PIL import Image, ImageTk
import time
import thread
from source.controller.process_people_counter import PC_Manager
from source.gui.frm_main import FrmMain

__author__ = 'huybu'
import Tkinter as tk

import sys
# import imp
# PC_Manager = imp.load_source('PC_Manager', '../controller/process_people_counter')
# FrmMain = imp.load_source('FrmMain', './frm_main')

class ThreadedClient:
    def __init__(self, root_tk):
        self.root = root_tk
        self.queue_update_pc = multiprocessing.Queue()
        # Set up the GUI part
        self.frm_main = FrmMain(root_tk, self)
        self.lock = threading.Lock()
        self.lstProcess = []
        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)

    def remove_client(self, ip_address):
        self.frm_main.remove_client(ip_address)
        for p in self.lstProcess:
            if isinstance(p,PC_Manager):
                if p.ip_address is ip_address:
                    self.lstProcess.remove(p)
                    return

    def create_camera(self, ip_address, name_cam, macid):
        p = PC_Manager(ip_address, self, self.root, self.lock, self.queue_update_pc, name_cam, macid)
        self.lstProcess.append(p)
        p.start()

    def on_closing(self):
        try:
            for p in self.lstProcess:
                p.stop()
        except:
            pass
        try:
            root.destroy()
            root.quit()
        except:
            pass
        try:
            os.kill(os.getpid(),9)
        except:
            print 'can not self kill PROCESS'
            pass

if __name__ == "__main__":
    root = tk.Tk()
    client = ThreadedClient(root)
    root.mainloop()