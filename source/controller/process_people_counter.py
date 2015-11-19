import threading
import cv2
import time
from source.gui.frm_camera import FrmCamera
import socket
import multiprocessing
import sys
import numpy
from source.utils import const
from source.utils.depthmapCalculator import DepthmapCalculator
from source.utils.videoStreamer import VideoStreamer
from source.utils.backgroundSubtraction import BackgroundSubtraction
from source.utils.ObjectMoving import ObjectMoving
from source.utils.detectObject import DetectMoving
from source.utils.trackingObject import TrackingObj
import numpy as np
import cv2
from source.learningMachine.detect import Detector

class PC_Manager(object):
    def __init__(self,ip_address,root_tk,lock):
        self.ip_address = ip_address
        self.queue_process_to_frm = multiprocessing.Queue()
        self.queue_thread_to_process = multiprocessing.Queue()
        self.root = root_tk
        self.frm_camera = FrmCamera(self.root, lock,self.queue_process_to_frm)
        self.lock = lock
        # create process
        self.process_pc = Process_People_Counter(self.ip_address,self.queue_process_to_frm)

    def start(self):
        self.process_pc.start()
        self.frm_camera.toplevel.after(0, func=lambda: self.frm_camera.update_video())

class Process_People_Counter(multiprocessing.Process):
    def __init__(self, ip_address,queue_process_to_frm):
        multiprocessing.Process.__init__(self)
        self.ip_address = ip_address
        self.queue_process_to_frm = queue_process_to_frm
        self.running = True

    def run(self):
        print "I'm here " + self.ip_address
        # create dgram udp socket
        try:
            self.pi_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error:
            print 'Failed to create socket'
            return

        # load calibration data to calculate depth map
        depthmapCalculator = DepthmapCalculator('../../data/calibration')

        # calibrate camera
        calibration = depthmapCalculator.get_calibration()

        # init block matcher (SGBM) to calculate depth map
        block_matcher = depthmapCalculator.get_block_macher()

        # init background subtraction
        backgroundSubtraction = BackgroundSubtraction()

        # init detector
        detector = Detector(min_window_size=(150, 150), step_size=(30, 30), downscale=1)

        #init tracking
        trackObj = TrackingObj()

        # subtract moving object
        imgObjectMoving = ObjectMoving(150,150,30)

        detectMoving = DetectMoving(150)

        # if videoStreamer.connect_pi():
        count = 0
        font = cv2.FONT_HERSHEY_SIMPLEX
        cdetect = 0

        try:
            # Set the whole string
            self.pi_socket.sendto(const.CMD_CONNECT, (self.ip_address, const.PORT))
            print 'send ok'
            while self.running:
                try:
                    t1 = time.time()
                    reply, addr = self.pi_socket.recvfrom(50000)
                    arr = reply.split('daicahuy')
                    dataRight = numpy.fromstring(arr[0], dtype='uint8')
                    dataLeft = numpy.fromstring(arr[1], dtype='uint8')
                    image_right = cv2.imdecode(dataRight, 1)
                    image_left = cv2.imdecode(dataLeft, 1)

                    depthmap = depthmapCalculator.calculate(image_left, image_right, block_matcher, calibration)
                    display = None
                    # cv2.imshow("depthmap", depthmap)
                    if count > 20:
                        mask, display = backgroundSubtraction.compute(depthmap)
                        # cv2.imshow("back1", mask)
                        # res,pon1,pon2 = imgObjectMoving.getImgObjectMoving(mask)
                        # if res:
                        #     # cv2.rectangle(display,pon1, pon2,(255,255,255), 2)
                        #     if count>74:
                        #         im_detected = detector.detect(display[pon1[1]:pon2[1],pon1[0]:pon2[0]])
                        #     # cv2.imshow("back", display)
                        #         cv2.imshow("back", im_detected)
                        trackObj.resetTracking()
                        data,data150 = detectMoving.detectObjectInImage(display)
                        # if len(data150) > 0:
                        #     for y in data150:
                        #         imgx = display[y[0][1]:y[1][1],y[0][0]:y[1][0]]
                        #         cv2.imwrite("Image/"+str(count)+'.jpg', imgx)

                        if len(data) > 0:
                            for x in data:
                                # print x[0], x[1]
                                # print x[1][0] - x[0][0], x[1][1] - x[0][1]
                                # ckObj = trackObj.check_Obj(x[0],x[2])
                                # if ckObj == False:
                                #     cdetect+=1
                                #     print cdetect
                                if detector.detect1(display,x[0],x[1],x[2]):
                                    trackObj.trackingObj(x[0],x[2])
                                    cv2.rectangle(image_left,x[0], x[1],(255,255,255), 1)
                                # else:
                                #     cv2.rectangle(display,x[0], x[1],(255,255,255), 2)
                        trackObj.remove_track()
                        cv2.line(display,(0,20),(352,20),(255,255,255),1)
                        cv2.line(display,(0,150),(352,150),(255,255,255),1)
                        cv2.line(display,(0,270),(352,270),(255,255,255),1)
                        cv2.putText(display,'In: %i'%trackObj.InSh,(50,180), font, 0.5,(255,255,255),1)
                        cv2.putText(display,'Out: %i'%trackObj.OutSh,(200,180), font, 0.5,(255,255,255),1)
                        cv2.imshow("back", display)

                    # print "-----------------------------" + str(count)

                    # if res:
                    #     cv2.rectangle(display,pon1, pon2,(255,255,255), 2)

                    count+=1
                    char = cv2.waitKey(1)
                    if (char == 99):
                    #     count += 1
                    #     cv2.imwrite(str(count)+'.jpg', display)
                        print trackObj.InSh,trackObj.OutSh
                        cv2.waitKey(0)
                    if (char == 27):
                        break

                    self.queue_process_to_frm.put(display)
                    cv2.waitKey(1)
                    print 'fps = ' + str(1/(time.time()-t1))
                except Exception, ex:
                    print 'Thread_Listening_Socket Exception: ' + str(ex)

        except Exception, ex:
            print 'Thread_Listening_Socket Exception: ' + str(ex)
        # cap = cv2.VideoCapture(int(self.ip_address))
        # while True:
        #     try:
        #         ret,frame = cap.read()
        #         self.queue_process_to_frm.put(frame)
        #         cv2.waitKey(1)
        #     except Exception, ex:
        #         print 'thread_camera Exception: ' + str(ex)
