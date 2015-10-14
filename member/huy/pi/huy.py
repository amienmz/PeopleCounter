import threading
# import test
import huy
from pc_client import huy
__author__ = 'huybu'
# import const
#
# line = 'huydaicahuyhehe'
#
# ar = line.split('daicahuy')
#
# print(ar)
#
# print(const.POS_DATA)

# class huy(threading.Thread):
#     def __init__(self, value):
#         super(huy, self).__init__()
#         self.valuee = value
#         return
#     def run(self):
#         for i in range(self.valuee):
#             print(str(i) + ' ')


client = huy(10)
client.start()