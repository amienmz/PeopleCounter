import threading
# import test

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

class huy(threading.Thread):
    def __init__(self, value):
        self.valuee = value
        return
    def run(self):
        for i in range(0, self.valuee):
            print(i + ' ')


client = huy(10)
client.start()