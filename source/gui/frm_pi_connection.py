__author__ = 'huybu'
import Tkinter as tk


class FrmPiConnection(object):
    def __init__(self, parent):
        self.toplevel = tk.Toplevel(parent)
        self.var = tk.StringVar()
        tk.Label(self.toplevel, text='Input ip address of PI:').pack(side=tk.LEFT, padx=10, pady=10)
        self.entry = tk.Entry(self.toplevel, textvariable=self.var, width=21)
        self.entry.pack(side=tk.LEFT, pady=10, padx=10)
        button = tk.Button(self.toplevel, text="OK", command=self.toplevel.destroy)
        button.pack()

    def show(self):
        self.toplevel.deiconify()
        self.toplevel.wait_window()
        return self.var.get()
