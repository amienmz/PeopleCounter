import cv2
import numpy
import time
import zlib
import const
import socket  # for sockets
import sys  # for exit

class VideoStreamer(object):

    # def __init__(self, host, port):
    #     # create dgram udp socket
    #     try:
    #         self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #     except socket.error:
    #         print 'Failed to create socket'
    #         sys.exit()
    #
    #     # HOST = '10.20.13.171';
    #     self.host = host
    #     self.port = port;

    def __init__(self, video_left, video_right):
        self.link_video_left = video_left
        self.link_video_right = video_right

    # def connect_pi(self):
    #     try:
    #         self.s.sendto(const.CMD_CONNECT,(self.host, self.port))
    #         return True
    #     except socket.error, msg:
    #         print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    #     return False

    # def get_image_from_pi(self):
    #     try:
    #         d = self.s.recvfrom(50000)
    #         reply = zlib.decompress(d[0])
    #         addr = d[1]
    #         arr = reply.split('daicahuy')
    #         dataRight = numpy.fromstring(arr[0], dtype='uint8')
    #         dataLeft = numpy.fromstring(arr[1], dtype='uint8')
    #         decimgRight = cv2.imdecode(dataRight, 1)
    #         decimgLeft = cv2.imdecode(dataLeft, 1)
    #         return decimgLeft, decimgRight
    #     except:
    #         print 'Exception: ' + sys.exc_info()[0]
    #         pass
    #     return None, None

    def get_video_data(self):
        videoLeft = cv2.VideoCapture(self.link_video_left) #right
        videoLeft.set(3,352)
        videoLeft.set(4,288)

        videoRight = cv2.VideoCapture(self.link_video_right)
        videoRight.set(3,352)
        videoRight.set(4,288)

        return videoLeft, videoRight

    def get_image_from_video(self, video_left, video_right):
        ret1, frameLeft = video_left.read()
        ret2, frameRight = video_right.read()
        return frameLeft, frameRight