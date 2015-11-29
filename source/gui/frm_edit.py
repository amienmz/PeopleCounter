import tkMessageBox

__author__ = 'pc'
from Tkinter import *

class FrmEdit(object):
    def __init__(self, parent, infor):
        self.toplevel = Toplevel(parent)
        self.strEntryName = StringVar()
        self.create_gui(self.toplevel)
        arr = infor.split('-')
        self.ip = arr[1]
        self.entry_name.delete(0,END)
        self.entry_name.insert(0,arr[0])
        self.lblInfor["text"] = str(infor)
        self.ret = False

    def show(self):
        self.toplevel.deiconify()
        self.toplevel.wait_window()
        return self.ret, self.strEntryName.get()+'-'+self.ip

    def btnOk_click(self):
        if not self.strEntryName.get().strip():
            tkMessageBox.showerror("Bad data!","Please input Name")
            self.request_focus()
            return
        if '-' in self.strEntryName.get().strip():
            tkMessageBox.showerror("Bad data!","Please don't use '-' character in Name")
            self.request_focus()
            return
        self.ret = True
        self.toplevel.destroy()

    def request_focus(self):
        self.toplevel.wm_attributes("-topmost", 1)
        self.toplevel.focus_force()
        self.toplevel.wm_attributes("-topmost", 0)

    def create_gui(self, master):
        master.title('Edit')
        geom = "283x102+409+221"
        master.geometry(geom)
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#d9d9d9'  # X11 color: 'gray85'
        master.configure(background="#d9d9d9")
        self.Label1 = Label(master)
        self.Label1.place(relx=0.04, rely=0.39, height=21, width=41)
        self.Label1.configure(background=_bgcolor)
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''Name:''')

        self.lblInfor = Label(master)
        self.lblInfor.place(relx=0.04, rely=0.1, height=21, width=264)
        self.lblInfor.configure(background=_bgcolor)
        self.lblInfor.configure(disabledforeground="#a3a3a3")
        self.lblInfor.configure(foreground="#000000")
        self.lblInfor.configure(text='''lable''')

        self.entry_name = Entry(master, textvariable=self.strEntryName)
        self.entry_name.place(relx=0.21, rely=0.39, relheight=0.2, relwidth=0.76)
        self.entry_name.configure(background="white")
        self.entry_name.configure(disabledforeground="#a3a3a3")
        self.entry_name.configure(font="TkFixedFont")
        self.entry_name.configure(foreground="#000000")
        self.entry_name.configure(insertbackground="black")
        self.entry_name.configure(width=214)


        self.btnOk = Button(master)
        self.btnOk.place(relx=0.8, rely=0.69, height=24, width=47)
        self.btnOk.configure(activebackground="#d9d9d9")
        self.btnOk.configure(activeforeground="#000000")
        self.btnOk.configure(background=_bgcolor)
        self.btnOk.configure(command=self.btnOk_click)
        self.btnOk.configure(disabledforeground="#a3a3a3")
        self.btnOk.configure(foreground="#000000")
        self.btnOk.configure(highlightbackground="#d9d9d9")
        self.btnOk.configure(highlightcolor="black")
        self.btnOk.configure(pady="0")
        self.btnOk.configure(text='''OK''')
