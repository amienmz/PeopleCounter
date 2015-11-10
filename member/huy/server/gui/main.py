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
from member.huy.server.controller.process_people_counter import Process_People_Counter, PC_Manager


class ThreadedClient:
    def __init__(self, root_tk):
        self.root = root_tk
        # Set up the GUI part
        self.frm_main = FrmMain(root_tk, self)
        self.lock = threading.Lock()

    def create_camera(self, ip_address):
        p = PC_Manager(ip_address, self.root, self.lock)
        p.start()


if __name__ == "__main__":
    root = tk.Tk()
    client = ThreadedClient(root)
    root.mainloop()
