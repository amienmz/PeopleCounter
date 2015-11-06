import Queue
from multiprocessing import Process
import threading
import cv2
from PIL import Image, ImageTk
import time
import thread
__author__ = 'huybu'
import Tkinter as tk
from frm_main import FrmMain
from frm_camera import FrmCamera
import socket  # for sockets
from member.huy.server.controller.process_streamer import Process_Streamer,Streamer

class ThreadedClient:

    def __init__(self, root_tk):
        self.root = root_tk
        # Set up the GUI part
        self.frm_main = FrmMain(root_tk, self)
        self.lst_frm_camera = []
        self.lock = threading.Lock()

    def create_socket(self):
        # create dgram udp socket
        try:
            self.pi_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error:
            print 'Failed to create socket'

    def create_camera(self,ip_address):
        p = Streamer(ip_address,self.root,self.lock)
        p.start()

if __name__ == "__main__":
    root = tk.Tk()
    client = ThreadedClient(root)
    root.mainloop()
