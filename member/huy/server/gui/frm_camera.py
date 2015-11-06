__author__ = 'huybu'
import Tkinter as tk
import cv2
import Tkinter
from PIL import Image, ImageTk

class FrmCamera(object):
    def __init__(self, parent,lock):
        self.toplevel = tk.Toplevel(parent)
        self.lock = lock
        self.var = tk.StringVar()
        print 'GUI initialized...'
        self.image_label = tk.Label(self.toplevel)  # label for the video frame
        self.image_label.pack()

    def show(self):
        self.toplevel.deiconify()
        self.toplevel.wait_window()
        return self.var.get()

    def update_video(self, queue):
                # frame = queue.get()
                # im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # a = Image.fromarray(im)
                # b = ImageTk.PhotoImage(image=a)
                # self.image_label.configure(image=b)
                # self.image_label._image_cache = b  # avoid garbage collection
                # self.toplevel.update()
                # cv2.waitKey(1)
        try:
            # self.lock.acquire
            with self.lock:
                frame = queue.get()
                im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                a = Image.fromarray(im)
                b = ImageTk.PhotoImage(image=a)
                self.image_label.configure(image=b)
                self.image_label._image_cache = b  # avoid garbage collection
                self.toplevel.update()
                cv2.waitKey(1)
                self.toplevel.after(0, func=lambda: self.update_video(queue))
        except Exception, ex:
            print 'frm_camera update_video Exception: ' + str(ex)
        # finally:
        #     self.lock.release()
