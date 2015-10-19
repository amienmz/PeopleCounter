import threading
# import test
import cv2
import time
import huy
# from pc_client import huy
# __author__ = 'huybu'
# # import const
# #
# # line = 'huydaicahuyhehe'
# #
# # ar = line.split('daicahuy')
# #
# # print(ar)
# #
# # print(const.POS_DATA)
#
# # class huy(threading.Thread):
# #     def __init__(self, value):
# #         super(huy, self).__init__()
# #         self.valuee = value
# #         return
# #     def run(self):
# #         for i in range(self.valuee):
# #             print(str(i) + ' ')
#
#
# client = huy(10)
# client.start()

cap = cv2.VideoCapture(0)
cap.set(3,352)
cap.set(4,352)

while True:
    first = time.time()
    ret, frame = cap.read()
    cv2.imshow('pro',frame)
    print "time = " + str(time.time()-first)
    cv2.waitKey(1)