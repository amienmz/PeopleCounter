from multiprocessing import Process
import numpy

__author__ = 'huybu'
import Tkinter as tk
from frm_pi_connection import FrmPiConnection
import socket
import source.utils.const as const
import cv2

class FrmMain(tk.Frame):
    def __init__(self, parent, threadClient):
        tk.Frame.__init__(self, parent)

        self.create_gui(parent)
        self.create_socket()
        self.threadClient = threadClient

    def create_socket(self):
        # create dgram udp socket
        try:
            self.pi_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error:
            print 'Failed to create socket'


    def create_gui(self, parent):
        # panel
        self.pnl_left = tk.Frame(parent, bg="")
        self.pnl_right = tk.Frame(parent, bg="")
        self.pnl_left.pack(side=tk.LEFT, anchor=tk.W, fill=tk.Y)
        self.pnl_right.pack(side=tk.RIGHT, anchor=tk.E, fill=tk.Y)
        # create in left panel
        self.lb_cam = tk.Listbox(self.pnl_left)
        self.lb_cam.pack(side=tk.LEFT)
        # lb_cam.insert(tk.END, "a list entry")
        # for item in ["one", "two", "three", "four"]:
        #     lb_cam.insert(tk.END, item)
        # create in right panel
        # topright_panel = tk.Frame(right_panel, bg="blue")
        # bottomright_panel = tk.Frame(right_panel, bg="blue")
        # topright_panel.pack(side=tk.TOP,anchor=tk.N)
        # bottomright_panel.pack( side=tk.BOTTOM,anchor=tk.S )
        # insert_button = tk.Button(topright_panel,text="Insert")
        # insert_button.pack(side=tk.LEFT)
        # show_button = tk.Button(topright_panel,text="Show")
        # show_button.pack(side=tk.LEFT)
        #
        # test_button = tk.Button(bottomright_panel,text="Test")
        # test_button.pack()
        self.txt_total_in = tk.StringVar()
        self.lbl_total_in = tk.Label(self.pnl_right, textvariable=self.txt_total_in)
        self.txt_total_in.set("Total in:")
        self.lbl_total_in.pack()
        self.txt_total_out = tk.StringVar()
        self.lbl_total_out = tk.Label(self.pnl_right, textvariable=self.txt_total_out)
        self.txt_total_out.set("Total out:")
        self.lbl_total_out.pack()
        self.btn_insert = tk.Button(self.pnl_right, text="Insert", command=self.insert_click)
        self.btn_insert.pack()
        self.btn_show = tk.Button(self.pnl_right, text="Show", command=self.show_click)
        self.btn_show.pack()
        self.btn_hide = tk.Button(self.pnl_right, text="Hide")
        self.btn_hide.pack()
        self.btn_kill = tk.Button(self.pnl_right, text="Kill")
        self.btn_kill.pack()

    def show_click(self):
        p = Process(target=self.test_process)
        p.start()

    def test_process(self):
        print 'process OK'

    def insert_click(self):
        ip_address = FrmPiConnection(self).show()
        print ip_address
        self.threadClient.create_camera(ip_address)


    def image_capture(queue):
       vidFile = cv2.VideoCapture(0)
       while True:
          try:
             flag, frame=vidFile.read()
             if flag==0:
                break
             queue.put(frame)
             cv2.waitKey(20)
          except:
             continue

    def pi_execute(self,ip_address,pi_socket):
        try:
            # Set the whole string
            pi_socket.sendto(const.CMD_CONNECT, (ip_address, const.PORT))

            # receive data from client (data, addr)
            first = None
            while True:
                # try:
                    d = pi_socket.recvfrom(50000)
                    reply = (d[0])
                    # reply = d[0]
                    addr = d[1]
                    arr = reply.split('daicahuy')
                    dataRight = numpy.fromstring(arr[0], dtype='uint8')
                    dataLeft = numpy.fromstring(arr[1], dtype='uint8')
                    decimgRight = cv2.imdecode(dataRight, 1)
                    decimgLeft = cv2.imdecode(dataLeft, 1)
                    cv2.imshow('SERVER RIGHT', decimgRight)
                    cv2.imshow('SERVER LEFT', decimgLeft)
                    # duration = (time.time() - first)
                    # print " pp: " + str(count / duration) + " p/s" + " duration = " + str(duration)
                    cv2.waitKey(1)
                # except:
                #     print 'Exception: ' + sys.exc_info()[0]
                #     pass


        except socket.error, msg:
            print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            # sys.exit()