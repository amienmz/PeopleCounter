from multiprocessing import Process
from re import search
import numpy
from numpy.lib.function_base import insert
from threading import Thread
from controller.process_people_counter import PC_Manager

__author__ = 'huybu'

from Tkinter import *
import ttk
py3 = 0
from frm_pi_connection import FrmPiConnection
import socket
import source.utils.const as const
import cv2


class FrmMain(Frame):
    def __init__(self, master, threadClient):
        Frame.__init__(self, master)
        self.create_gui(master)
        self.create_socket()
        self.threadClient = threadClient
        master.wm_title("People Counter")
        self.thread = Thread(target = self.wait_value_queue)
        self.thread.start()
        # self.lbCameras.insert(END, 'huy'+ '- 123.123.123.123')
        # self.lbCameras.insert(END, 'pc'+ '- 123.123.123.123')


    def wait_value_queue(self):
        while True:
            type = self.threadClient.queue_update_pc.get()
            self.master.after(0, func=lambda: self.update_gui(type))

    def update_gui(self, type):
        peopleIn = int(self.lblIn["text"])
        peopleOut = int(self.lblOut["text"])
        if type == const.TYPE_IN:
            peopleIn+=1
            self.lblIn["text"] = str(peopleIn)
            pass
        if type == const.TYPE_OUT:
            peopleOut+=1
            self.lblOut["text"] = str(peopleOut)
            pass
        self.lblStay["text"] = str(peopleIn-peopleOut)
        self.master.update()

    def btnKill_click(self):
        try:
            curPI = str(self.lbCameras.get(self.lbCameras.curselection()))
            self.lbCameras.delete(self.lbCameras.curselection())
        except Exception, ex:
            print('frmMain.btnKill_click ' + str(ex))
            pass
        for p in self.threadClient.lstProcess:
            if p.ip_address in curPI:
                self.remove_client(p.ip_address)
                p.stop()

    def create_socket(self):
        # create dgram udp socket
        try:
            self.pi_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error:
            print 'Failed to create socket'

    def insert_cam(self, ip_address, name):
        self.lbCameras.insert(END, name+ '-' + ip_address)
        self._root().update()

    def insert_click(self):
        ret, ip_address, name_cam = FrmPiConnection(self,self.lbCameras).show()
        if not ret:
            return
        if ip_address and name_cam:
            print ip_address
            self.threadClient.create_camera(ip_address, name_cam)
            self.insert_cam(ip_address,name_cam)

    def remove_client(self, ip_address):
        index =0
        for str in list(self.lbCameras.get(0,END)):
            if ip_address in str:
                self.lbCameras.delete(index)
                return
            index+=1

    def create_gui(self, master):
        geom = "395x305+677+267"
        master.geometry(geom)
        # panel
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#d9d9d9' # X11 color: 'gray85'
        font10 = "-family {Segoe UI} -size 14 -weight normal -slant "  \
            "roman -underline 0 -overstrike 0"
        font12 = "-family {Courier New} -size 12 -weight normal -slant"  \
            " roman -underline 0 -overstrike 0"
        master.configure(background="#d9d9d9")


        self.lbCameras = Listbox(master)
        self.lbCameras.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=0.54)
        self.lbCameras.configure(background="white")
        self.lbCameras.configure(disabledforeground="#a3a3a3")
        self.lbCameras.configure(font=font12)
        self.lbCameras.configure(foreground="#000000")
        self.lbCameras.configure(width=214)

        self.Label1 = Label(master)
        self.Label1.place(relx=0.7, rely=0.07, height=31, width=31)
        self.Label1.configure(background=_bgcolor)
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font=font10)
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''In :''')

        self.Label2 = Label(master)
        self.Label2.place(relx=0.66, rely=0.16, height=31, width=46)
        self.Label2.configure(background=_bgcolor)
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(font=font10)
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''Out :''')

        self.btnShow = Button(master)
        self.btnShow.place(relx=0.61, rely=0.79, height=24, width=50)
        self.btnShow.configure(activebackground="#d9d9d9")
        self.btnShow.configure(activeforeground="#000000")
        self.btnShow.configure(background=_bgcolor)
        self.btnShow.configure(disabledforeground="#a3a3a3")
        self.btnShow.configure(foreground="#000000")
        self.btnShow.configure(highlightbackground="#d9d9d9")
        self.btnShow.configure(highlightcolor="black")
        self.btnShow.configure(pady="0")
        self.btnShow.configure(text='''Show''')
        self.btnShow.configure(width=50)

        self.btnHide = Button(master)
        self.btnHide.place(relx=0.61, rely=0.89, height=24, width=50)
        self.btnHide.configure(activebackground="#d9d9d9")
        self.btnHide.configure(activeforeground="#000000")
        self.btnHide.configure(background=_bgcolor)
        self.btnHide.configure(disabledforeground="#a3a3a3")
        self.btnHide.configure(foreground="#000000")
        self.btnHide.configure(highlightbackground="#d9d9d9")
        self.btnHide.configure(highlightcolor="black")
        self.btnHide.configure(pady="0")
        self.btnHide.configure(text='''Hide''')
        self.btnHide.configure(width=46)

        self.btnKill = Button(master, command=self.btnKill_click)
        self.btnKill.place(relx=0.76, rely=0.89, height=24, width=50)
        self.btnKill.configure(activebackground="#d9d9d9")
        self.btnKill.configure(activeforeground="#000000")
        self.btnKill.configure(background=_bgcolor)
        self.btnKill.configure(disabledforeground="#a3a3a3")
        self.btnKill.configure(foreground="#000000")
        self.btnKill.configure(highlightbackground="#d9d9d9")
        self.btnKill.configure(highlightcolor="black")
        self.btnKill.configure(pady="0")
        self.btnKill.configure(text='''Kill''')
        self.btnKill.configure(width=47)

        self.Label3 = Label(master)
        self.Label3.place(relx=0.66, rely=0.26, height=31, width=50)
        self.Label3.configure(background=_bgcolor)
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(font=font10)
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(text='''Stay :''')

        self.lblIn = Label(master)
        self.lblIn.place(relx=0.81, rely=0.07, height=31, width=16)
        self.lblIn.configure(background=_bgcolor)
        self.lblIn.configure(disabledforeground="#a3a3a3")
        self.lblIn.configure(font=font10)
        self.lblIn.configure(foreground="#000000")
        self.lblIn.configure(text='''0''')

        self.lblOut = Label(master)
        self.lblOut.place(relx=0.81, rely=0.16, height=31, width=16)
        self.lblOut.configure(background=_bgcolor)
        self.lblOut.configure(disabledforeground="#a3a3a3")
        self.lblOut.configure(font=font10)
        self.lblOut.configure(foreground="#000000")
        self.lblOut.configure(text='''0''')

        self.lblStay = Label(master)
        self.lblStay.place(relx=0.81, rely=0.26, height=31, width=16)
        self.lblStay.configure(background=_bgcolor)
        self.lblStay.configure(disabledforeground="#a3a3a3")
        self.lblStay.configure(font=font10)
        self.lblStay.configure(foreground="#000000")
        self.lblStay.configure(text='''0''')

        self.btnInsert = Button(master, command=self.insert_click)
        self.btnInsert.place(relx=0.76, rely=0.79, height=24, width=50)
        self.btnInsert.configure(activebackground="#d9d9d9")
        self.btnInsert.configure(activeforeground="#000000")
        self.btnInsert.configure(background=_bgcolor)
        self.btnInsert.configure(disabledforeground="#a3a3a3")
        self.btnInsert.configure(foreground="#000000")
        self.btnInsert.configure(highlightbackground="#d9d9d9")
        self.btnInsert.configure(highlightcolor="black")
        self.btnInsert.configure(pady="0")
        self.btnInsert.configure(text='''Insert''')
        self.btnInsert.configure(width=50)
