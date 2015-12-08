from multiprocessing import Process
from re import search
import numpy
from numpy.lib.function_base import insert
from threading import Thread
from controller.process_people_counter import PC_Manager
from frm_edit import FrmEdit

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
        self.threadClient = threadClient
        master.wm_title("People Counter")

        # wait to get data of in/out people from process execute count people
        self.thread_update_inout = Thread(target=self.wait_people_inout)
        self.thread_update_inout.start()
        # self.lbCameras.insert(END, 'huy'+ '- 123.123.123.123')
        # self.lbCameras.insert(END, 'pc'+ '- 123.123.123.123')

    def wait_people_inout(self):
        while True:
            in_out = self.threadClient.queue_update_pc.get()
            self.master.after(0, func=lambda: self.update_gui(in_out))

    def update_gui(self, in_out):
        peopleIn = int(self.lblIn["text"])
        peopleOut = int(self.lblOut["text"])
        if in_out == const.TYPE_IN:
            peopleIn += 1
            self.lblIn["text"] = str(peopleIn)
            pass
        if in_out == const.TYPE_OUT:
            peopleOut += 1
            self.lblOut["text"] = str(peopleOut)
            pass
        self.lblStay["text"] = str(peopleIn - peopleOut)
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

    def insert_cam(self, ip_address, name):
        self.lbCameras.insert(END, name + '-' + ip_address)
        self._root().update()

    def btnInsert_click(self):
        ret, ip_address, name_cam, macid, isDevMode = FrmPiConnection(self, self.lbCameras).show()
        if not ret:
            return
        if ip_address and name_cam:
            print ip_address
            self.threadClient.create_camera(ip_address, name_cam, macid, isDevMode)
            self.insert_cam(ip_address, name_cam)

    def remove_client(self, ip_address):
        index = 0
        for str in list(self.lbCameras.get(0, END)):
            if ip_address in str:
                self.lbCameras.delete(index)
                return
            index += 1

    def btnClose_click(self):
        self.threadClient.on_closing()

    def btnEdit_click(self):
        try:
            index = self.lbCameras.curselection()
            infor = str(self.lbCameras.get(index))
            ret, new_infor = FrmEdit(self, infor).show()
            if ret:
                self.lbCameras.delete(index)
                self.lbCameras.insert(index, new_infor)
            for p in self.threadClient.lstProcess:
                if p.ip_address in infor:
                    p.queue_execute_data.put(const.CHANGE_NAME)
                    p.queue_execute_data.put(new_infor.split('-')[0])
        except Exception, ex:
            print('frmMain.btnEdit_click ' + str(ex))


    def create_gui(self, master):
        geom = "395x305+677+267"
        master.geometry(geom)
        # panel
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#d9d9d9'  # X11 color: 'gray85'
        font10 = "-family {Segoe UI} -size 14 -weight normal -slant " \
                 "roman -underline 0 -overstrike 0"
        font12 = "TkDefaultFont"
        master.configure(background="#d9d9d9")
        master.configure(highlightbackground="#d9d9d9")
        master.configure(highlightcolor="black")

        self.lbCameras = Listbox(master)
        self.lbCameras.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=0.54)
        self.lbCameras.configure(background="white")
        self.lbCameras.configure(disabledforeground="#a3a3a3")
        font12 = "-family Arial -size 12 -weight normal -slant roman " \
                 "-underline 0 -overstrike 0"
        self.lbCameras.configure(font=font12)
        self.lbCameras.configure(foreground="#000000")
        self.lbCameras.configure(highlightbackground="#d9d9d9")
        self.lbCameras.configure(highlightcolor="black")
        self.lbCameras.configure(selectbackground="#c4c4c4")
        self.lbCameras.configure(selectforeground="black")

        self.Label1 = Label(master)
        self.Label1.place(relx=0.7, rely=0.07, height=31, width=31)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(background=_bgcolor)
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font=font10)
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''In :''')

        self.Label2 = Label(master)
        self.Label2.place(relx=0.66, rely=0.16, height=31, width=46)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(activeforeground="black")
        self.Label2.configure(background=_bgcolor)
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(font=font10)
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black")
        self.Label2.configure(text='''Out :''')

        self.btnInsert2 = Button(master)
        self.btnInsert2.place(relx=0.61, rely=0.79, height=24, width=50)
        self.btnInsert2.configure(activebackground="#d9d9d9")
        self.btnInsert2.configure(activeforeground="#000000")
        self.btnInsert2.configure(background=_bgcolor)
        self.btnInsert2.configure(command=self.btnInsert_click)
        self.btnInsert2.configure(disabledforeground="#a3a3a3")
        self.btnInsert2.configure(foreground="#000000")
        self.btnInsert2.configure(highlightbackground="#d9d9d9")
        self.btnInsert2.configure(highlightcolor="black")
        self.btnInsert2.configure(pady="0")
        self.btnInsert2.configure(text='''Insert''')

        self.btnKill2 = Button(master)
        self.btnKill2.place(relx=0.61, rely=0.89, height=24, width=50)
        self.btnKill2.configure(activebackground="#d9d9d9")
        self.btnKill2.configure(activeforeground="#000000")
        self.btnKill2.configure(background=_bgcolor)
        self.btnKill2.configure(command=self.btnKill_click)
        self.btnKill2.configure(disabledforeground="#a3a3a3")
        self.btnKill2.configure(foreground="#000000")
        self.btnKill2.configure(highlightbackground="#d9d9d9")
        self.btnKill2.configure(highlightcolor="black")
        self.btnKill2.configure(pady="0")
        self.btnKill2.configure(text='''Kill''')

        self.btnClose = Button(master)
        self.btnClose.place(relx=0.76, rely=0.89, height=24, width=50)
        self.btnClose.configure(activebackground="#d9d9d9")
        self.btnClose.configure(activeforeground="#000000")
        self.btnClose.configure(background=_bgcolor)
        self.btnClose.configure(command=self.btnClose_click)
        self.btnClose.configure(disabledforeground="#a3a3a3")
        self.btnClose.configure(foreground="#000000")
        self.btnClose.configure(highlightbackground="#d9d9d9")
        self.btnClose.configure(highlightcolor="black")
        self.btnClose.configure(pady="0")
        self.btnClose.configure(text='''Close''')

        self.Label3 = Label(master)
        self.Label3.place(relx=0.66, rely=0.26, height=31, width=50)
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(activeforeground="black")
        self.Label3.configure(background=_bgcolor)
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(font=font10)
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(highlightbackground="#d9d9d9")
        self.Label3.configure(highlightcolor="black")
        self.Label3.configure(text='''Stay :''')

        self.lblIn = Label(master)
        self.lblIn.place(relx=0.81, rely=0.07, height=31, width=56)
        self.lblIn.configure(activebackground="#f9f9f9")
        self.lblIn.configure(activeforeground="black")
        self.lblIn.configure(background=_bgcolor)
        self.lblIn.configure(disabledforeground="#a3a3a3")
        self.lblIn.configure(font=font10)
        self.lblIn.configure(foreground="#000000")
        self.lblIn.configure(highlightbackground="#d9d9d9")
        self.lblIn.configure(highlightcolor="black")
        self.lblIn.configure(text='''0''')

        self.lblOut = Label(master)
        self.lblOut.place(relx=0.81, rely=0.16, height=31, width=56)
        self.lblOut.configure(activebackground="#f9f9f9")
        self.lblOut.configure(activeforeground="black")
        self.lblOut.configure(background=_bgcolor)
        self.lblOut.configure(disabledforeground="#a3a3a3")
        self.lblOut.configure(font=font10)
        self.lblOut.configure(foreground="#000000")
        self.lblOut.configure(highlightbackground="#d9d9d9")
        self.lblOut.configure(highlightcolor="black")
        self.lblOut.configure(text='''0''')

        self.lblStay = Label(master)
        self.lblStay.place(relx=0.81, rely=0.26, height=31, width=56)
        self.lblStay.configure(activebackground="#f9f9f9")
        self.lblStay.configure(activeforeground="black")
        self.lblStay.configure(background=_bgcolor)
        self.lblStay.configure(disabledforeground="#a3a3a3")
        self.lblStay.configure(font=font10)
        self.lblStay.configure(foreground="#000000")
        self.lblStay.configure(highlightbackground="#d9d9d9")
        self.lblStay.configure(highlightcolor="black")
        self.lblStay.configure(text='''0''')

        self.btnEdit = Button(master)
        self.btnEdit.place(relx=0.76, rely=0.79, height=24, width=50)
        self.btnEdit.configure(activebackground="#d9d9d9")
        self.btnEdit.configure(activeforeground="#000000")
        self.btnEdit.configure(command=self.btnEdit_click)
        self.btnEdit.configure(background=_bgcolor)
        self.btnEdit.configure(disabledforeground="#a3a3a3")
        self.btnEdit.configure(foreground="#000000")
        self.btnEdit.configure(highlightbackground="#d9d9d9")
        self.btnEdit.configure(highlightcolor="black")
        self.btnEdit.configure(pady="0")
        self.btnEdit.configure(text='''Edit''')
