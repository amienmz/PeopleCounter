__author__ = 'huybu'
import cv2

# ('../../../Datas/outputR24.avi')
import cv2
import numpy as np

winname = "GRS"

bgs_mog = cv2.BackgroundSubtractorMOG(500, 6, 0.9, 1)

capture = cv2.VideoCapture('../../../Datas/outputR24.avi')

frame = capture.read()[1]

if __name__ == "__main__":
    while frame != None:
        fgmask = bgs_mog.apply(frame)
        cv2.imshow('mask', fgmask)
        cv2.imshow(winname, frame)
        c = cv2.waitKey(1)
        if c == 27:
            cv2.destroyWindow(winname)
            break
        frame = capture.read()[1]
    cv2.destroyAllWindows()