import Queue
import Tkinter as tk
import threading
import time


class MyDialog(object):
    def __init__(self, parent):
        self.toplevel = tk.Toplevel(parent)
        self.var = tk.StringVar()
        label = tk.Label(self.toplevel, text="Pick something:")
        om = tk.OptionMenu(self.toplevel, self.var, "one", "two","three")
        button = tk.Button(self.toplevel, text="OK", command=self.toplevel.destroy)
        label.pack(side="top", fill="x")
        om.pack(side="top", fill="x")
        button.pack()

    def show(self):
        self.toplevel.deiconify()
        self.toplevel.wait_window()
        value = self.var.get()
        return value


class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.button = tk.Button(self, text="Click me!", command=self.on_click)
        self.label = tk.Label(self, width=80)
        self.label.pack(side="top", fill="x")
        self.button.pack(pady=20)

    def on_click(self):
        result = MyDialog(self).show()
        self.label.configure(text="your result: %s" % result)
def f(q):
    while True:
        print q.get() #block thread until something shows up
if __name__ == "__main__":
    root = tk.Tk()
    # Example(root).pack(fill="both", expand=True)
    # root.mainloop()
    # tk.Label(text='Input ip address and port of PI:').pack(side=tk.LEFT,padx=10,pady=10)
    # entry = tk.Entry(root, width=21)
    # entry.pack(side=tk.LEFT,pady=10,padx=10)
    # root.mainloop()
    q = Queue.Queue()
    t = threading.Thread(target=f,args=[q])
    t.daemon = True #if parent dies, kill thread
    t.start()
    for x in range(0,1000):
        q.put(x)
        time.sleep(1)


