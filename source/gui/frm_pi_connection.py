import socket
from source.controller.process_people_counter import PC_Manager
from source.utils import const
from threading import Thread
__author__ = 'huybu'
from Tkinter import *
import ipaddress
from IPy import IP
import ttk
import tkMessageBox
class FrmPiConnection(object):
    def __init__(self, parent, lbCames):
        self.lbCames = lbCames
        self.toplevel = Toplevel(parent)
        self.strName = StringVar()
        self.running = True
        self.list_cam = []
        self.strEntryIp = StringVar()
        self.strCbb = StringVar()
        self.create_gui()
        self.ret = False

    def show(self):
        self.toplevel.deiconify()
        self.toplevel.wait_window()
        return self.ret, self.strEntryIp.get(), self.strName.get()

    def btnConnect_click(self):
        try:
            IP(self.strEntryIp.get())
            # print 'check size = ' + len(self.lstProcess)
            for str in list(self.lbCames.get(0,END)):
                if self.strEntryIp.get() in str:
                    tkMessageBox.showerror("Duplicate Connection!","This IP is already connected")
                    self.request_focus()
                    return
            # for p in self.lbCames:
            #     print p.ip_address
            #     if isinstance(p,PC_Manager):
            #         if p.ip_address is self.strEntryIp.get():
            #             tkMessageBox.showerror("Duplicate Connection!","This IP is already connected")
            #             self.request_focus()
            #             return
        except Exception,ex:
            print(str(ex))
            tkMessageBox.showerror("IP error!","Please input valid Ip Addrerss!")
            self.request_focus()
            return
        if not self.strName.get().strip():
            tkMessageBox.showerror("Name error!","Please input name!")
            self.request_focus()
            return
        self.ret = True
        self.toplevel.destroy()

    def request_focus(self):
        self.toplevel.wm_attributes("-topmost", 1)
        self.toplevel.focus_force()
        self.toplevel.wm_attributes("-topmost", 0)

    def btnRefresh_click(self):
        self.thread = Thread(target = self.run)
        self.thread.start()

    def stop(self):
        self.running = False
        # self.pi_socket.socket(socket.AF_INET,
        #               socket.SOCK_STREAM).connect( ('', 9999))
        self.pi_socket.close()

    def run(self):
        self.running = True
        self.list_cam = []
        try:
            self.pi_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.pi_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.pi_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        except socket.error:
            print 'Failed to create socket'
            return
        # Bind socket to local host and port
        try:
            self.pi_socket.bind(('', 9999))
        except socket.error, msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        try:
            # Set the whole string
            self.pi_socket.sendto(const.CMD_CHECK, ("255.255.255.255", const.PORT))
            print 'send ok'
            count = 0
            while self.running:
                count += 1
                print str(count)
                try:
                    reply, addr = self.pi_socket.recvfrom(50000)
                    self.list_cam.append(reply+'-'+addr[const.POS_IP])
                    # if reply == const.CMD_CHECK:
                    #     print addr[0]
                except Exception, ex:
                    print 'Thread_Listening_Socket TRUE Exception: ' + str(ex)

        except Exception, ex:
            print 'Thread_Listening_Socket Exception: ' + str(ex)

    def update_combobox(self):
        # self.cbbAvaibleCam['values'] = ('X', 'Y', 'Z')
        self.cbbAvaibleCam['values'] = self.list_cam
        if (len(self.list_cam)==1):
            value = self.list_cam[0]
            self.cbbAvaibleCam.current(0)
            # self.entryName.delete(0,END)
            self.entryIpAddress.delete(0,END)
            # self.entryName.insert(0,value.split('-')[0])
            self.entryIpAddress.insert(0,value.split('-')[1])
        self.toplevel.update()
        self.cbbAvaibleCam.after(1000, func=lambda: self.update_combobox())

    def cbbAvaible_selected(self, event):
        value = self.cbbAvaibleCam.get()
        # self.entryName.delete(0,END)
        self.entryIpAddress.delete(0,END)
        # self.entryName.insert(0,value.split('-')[0])
        self.entryIpAddress.insert(0,value.split('-')[1])

    def create_gui(self):
        self.toplevel.title('Pi_Connection')
        geom = "402x147+673+398"
        self.toplevel.geometry(geom)
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#d9d9d9'  # X11 color: 'gray85'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=
        [('selected', _compcolor), ('active', _ana2color)])
        self.toplevel.configure(background="#d9d9d9")
        self.Label1 = Label(self.toplevel)
        self.Label1.place(relx=0.01, rely=0.34, height=21, width=67)
        self.Label1.configure(background=_bgcolor)
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''IP Address :''')
        self.entryIpAddress = Entry(self.toplevel, textvariable=self.strEntryIp)
        self.entryIpAddress.place(relx=0.2, rely=0.35, relheight=0.14
                , relwidth=0.58)
        self.entryIpAddress.configure(background="white")
        self.entryIpAddress.configure(disabledforeground="#a3a3a3")
        self.entryIpAddress.configure(font="TkFixedFont")
        self.entryIpAddress.configure(foreground="#000000")
        self.entryIpAddress.configure(insertbackground="black")
        self.entryIpAddress.configure(width=184)

        self.btnConnect = Button(self.toplevel, command=self.btnConnect_click)
        self.btnConnect.place(relx=0.81, rely=0.34, height=24, width=56)
        self.btnConnect.configure(activebackground="#d9d9d9")
        self.btnConnect.configure(activeforeground="#000000")
        self.btnConnect.configure(background=_bgcolor)
        self.btnConnect.configure(disabledforeground="#a3a3a3")
        self.btnConnect.configure(foreground="#000000")
        self.btnConnect.configure(highlightbackground="#d9d9d9")
        self.btnConnect.configure(highlightcolor="black")
        self.btnConnect.configure(pady="0")
        self.btnConnect.configure(text='''Connect''')
        self.cbbAvaibleCam = ttk.Combobox(self.toplevel)
        self.cbbAvaibleCam.place(relx=0.2, rely=0.61, relheight=0.14
                , relwidth=0.58)
        self.cbbAvaibleCam.configure(textvariable=self.cbbAvaibleCam)
        self.cbbAvaibleCam.configure(width=183)
        self.cbbAvaibleCam.configure(takefocus="")
        self.cbbAvaibleCam.bind("<<ComboboxSelected>>", self.cbbAvaible_selected)

        self.btnRefresh = Button(self.toplevel)
        self.btnRefresh.place(relx=0.81, rely=0.61, height=24, width=56)
        self.btnRefresh.configure(activebackground="#d9d9d9")
        self.btnRefresh.configure(activeforeground="#000000")
        self.btnRefresh.configure(background=_bgcolor)
        self.btnRefresh.configure(command=self.btnRefresh_click)
        self.btnRefresh.configure(disabledforeground="#a3a3a3")
        self.btnRefresh.configure(foreground="#000000")
        self.btnRefresh.configure(highlightbackground="#d9d9d9")
        self.btnRefresh.configure(highlightcolor="black")
        self.btnRefresh.configure(pady="0")
        self.btnRefresh.configure(text='''Refesh''')
        self.btnRefresh.configure(width=56)
        self.Label2 = Label(self.toplevel)
        self.Label2.place(relx=0.02, rely=0.61, height=21, width=60)
        self.Label2.configure(background=_bgcolor)
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''Available :''')
        self.Label3 = Label(self.toplevel)
        self.Label3.place(relx=0.07, rely=0.11, height=21, width=44)
        self.Label3.configure(background=_bgcolor)
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(text='''Name :''')
        self.entryName = Entry(self.toplevel, textvariable=self.strName)
        self.entryName.place(relx=0.2, rely=0.1, relheight=0.14, relwidth=0.58)
        self.entryName.configure(background="white")
        self.entryName.configure(disabledforeground="#a3a3a3")
        self.entryName.configure(font="TkFixedFont")
        self.entryName.configure(foreground="#000000")
        self.entryName.configure(insertbackground="black")
        self.entryName.configure(width=184)
        self.cbbAvaibleCam.after(1000, func=lambda: self.update_combobox())
