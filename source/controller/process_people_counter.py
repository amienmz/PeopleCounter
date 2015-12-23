import requests
import threading
import cv2
import time
from source.gui.frm_camera import FrmCamera
import socket
import multiprocessing
import os
import numpy

from source.utils import const
from source.utils.depthmapCalculator import DepthmapCalculator
from source.utils.videoStreamer import VideoStreamer
from source.utils.backgroundSubtraction import BackgroundSubtraction
from source.utils.ObjectMoving import ObjectMoving
from source.utils.detectObject import DetectMoving
from source.utils.trackingObject import TrackingObj
import numpy as np
import cv2.cv
from source.learningMachine.detect import Detector
from utils import Object


class PC_Manager(object):
    def __init__(self, ip_address, threadClient, root_tk, lock, queue_update_pc, name_cam, macid, isDevMode):
        self.threadClient = threadClient
        self.ip_address = ip_address
        # self.webAdress = "http://10.20.13.180:3000/receiver"
        # self.queue_process_to_frm = multiprocessing.Queue()
        self.root = root_tk
        # self.frm_camera = FrmCamera(self.root, lock, self.queue_process_to_frm)
        self.lock = lock

        self.queue_execute_data = multiprocessing.Queue()
        self.running = True
        self.thread_execute_data = threading.Thread(target=self.wait_value_queue)

        # create process
        self.process_pc = Process_People_Counter(self.ip_address, queue_update_pc, self.queue_execute_data, isDevMode)
        self.name_cam = name_cam
        self.macid = macid

    def start(self):
        self.process_pc.start()
        self.thread_execute_data.start()
        # self.process_pc.join()
        # self.lock.acquire()
        # self.frm_camera.toplevel.after(0, func=lambda: self.frm_camera.update_video())
        # self.lock.release()

    def stop(self):
        self.running = False
        self.queue_execute_data.put(const.STOP_PROCESS)
        time.sleep(0.1)
        try:
            self.queue_execute_data.close()
        except Exception, ex:
            print 'STOP thread_wait_stop ' + str(ex)
            pass

        self.process_pc.stop()
        try:
            self.process_pc.terminate()
        except Exception, ex:
            print 'Process terminate exception ' + str(ex)
        try:
            self.process_pc.join()
        except Exception, ex:
            print 'Process join exception ' + str(ex)

    def wait_value_queue(self):
        # thread wait to romove PI and post data to web
        while self.running:
            try:
                value = self.queue_execute_data.get()

                if value == const.CHANGE_NAME:
                    self.name_cam = self.queue_execute_data.get()
                    print 'name_cam = ' + self.name_cam
                    payload = {'message': 'update_name', 'id': self.macid, 'name': self.name_cam}
                    r = requests.post(const.WEB_IP, data=payload)
                    print 'CHANGE_NAME'

                if value == const.CAMERAS_CONNECTED:
                    self.macid = self.queue_execute_data.get()
                    print 'macid = ' + self.macid
                    print 'name_cam = ' + self.name_cam
                    payload = {'message': 'update_status', 'id': self.macid, 'name': self.name_cam, 'status': 'true'}
                    r = requests.post(const.WEB_IP, data=payload)
                    print 'CAMERAS_CONNECTED'

                if value == const.STOP_PROCESS:
                    self.threadClient.remove_client(self.ip_address)
                    payload = {'message': 'update_status', 'id': self.macid, 'status': 'false'}
                    r = requests.post(const.WEB_IP, data=payload)
                    print 'STOP_PROCESS'

                if value == const.TYPE_IN:
                    payload = {'message': 'count', 'id': self.macid, 'is_come': 'true'}
                    r = requests.post(const.WEB_IP, data=payload)
                    print 'TYPE_IN'

                if value == const.TYPE_OUT:
                    payload = {'message': 'count', 'id': self.macid, 'is_come': 'false'}
                    r = requests.post(const.WEB_IP, data=payload)
                    print 'TYPE_OUT'
            except Exception, ex:
                print 'Thread wait_value_queue ' + str(ex)
                pass


class Process_People_Counter(multiprocessing.Process):
    def __init__(self, ip_address, queue_update_pc, queue_execute_data, isDevMode):
        multiprocessing.Process.__init__(self)
        self.ip_address = ip_address
        self.queue_update_pc = queue_update_pc
        self.running = True
        self.queue_execute_data = queue_execute_data
        self.isDevMode = isDevMode
        # create dgram udp socket
        try:
            self.pi_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error:
            print 'Failed to create socket'
            return

    def stop(self):
        print 'STOP PROCESS START'
        self.running = False
        try:
            self.pi_socket.sendto(const.CMD_DISCONNECT, (self.ip_address, const.PORT))
        except Exception, ex:
            print 'Process_People_Counter.STOP PI_SOCKET send disconect exception ???' + str(ex)
        try:
            socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(const.CMD_CONNECT, ('localhost', const.PORT))
        except Exception, ex:
            print 'Process_People_Counter.socket Exception ???' + str(ex)
        try:
            self.pi_socket.close()
        except Exception, ex:
            print 'Process_People_Counter.socket.close Exception???' + str(ex)
        try:
            self.queue_execute_data.put(const.STOP_PROCESS)
        except:
            pass
        print 'STOP PROCESS END'
        # try:
        #     os.kill(self.pid, 9)
        # except:
        #     pass

    def run(self):
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

        # init tracking
        trackObj = TrackingObj(self.queue_update_pc, self.queue_execute_data)

        # subtract moving object
        imgObjectMoving = ObjectMoving(150, 150, 30)

        detectMoving = DetectMoving(150)

        # if videoStreamer.connect_pi():
        count = 0
        font = cv2.FONT_HERSHEY_SIMPLEX
        cdetect = 0

        try:
            # Set the whole string
            port = const.PORT
            if ":" in self.ip_address:
                arr = self.ip_address.split(":")
                self.ip_address = arr[0]
                port = int(arr[1])
            self.pi_socket.sendto(const.CMD_CONNECT, (self.ip_address, port))
            self.pi_socket.settimeout(5)
            print 'send CMD_CONNECT ok to ' + self.ip_address

            # CODEC = cv2.cv.CV_FOURCC('M','P','4','V') # MPEG-4 = MPEG-1
            #
            # video_writer_right = cv2.VideoWriter("outputR24.avi", CODEC, 24, (352, 288))
            #
            # video_writer_left = cv2.VideoWriter("outputL24.avi", CODEC, 24, (352, 288))


            # detete old data before write image
            # os.system("rm -rf /home/pc/PycharmProjects/PeopleCounter/source/capture/pass/*")
            # os.system("rm -rf /home/pc/PycharmProjects/PeopleCounter/source/capture/fail/*")

            line_seperate = np.zeros((288, 5, 3), np.uint8) + 255
            devmod = None

            while self.running:
                t1 = time.time()
                reply, addr = self.pi_socket.recvfrom(50000)
                try:
                    if not const.JOIN in reply:
                        self.queue_execute_data.put(const.CAMERAS_CONNECTED)
                        self.queue_execute_data.put(reply)
                        continue
                    arr = reply.split(const.JOIN)
                    dataRight = numpy.fromstring(arr[0], dtype='uint8')
                    dataLeft = numpy.fromstring(arr[1], dtype='uint8')
                    image_right = cv2.imdecode(dataRight, 1)
                    image_left = cv2.imdecode(dataLeft, 1)
                    # cv2.imshow('SERVER RIGHT', image_right)
                    # cv2.imshow('SERVER LEFT', image_left)
                    # video_writer_right.write(image_right)
                    # video_writer_left.write(image_left)
                    # cv2.imwrite("../capture/video" + str(count) + ".jpg", image_left)
                    depthmap = depthmapCalculator.calculate(image_left, image_right, block_matcher, calibration)
                    # depthmap = 255 - depthmap
                    # cv2.imwrite("../capture/depth" + str(count) + ".jpg", depthmap)
                    if self.isDevMode == 1:
                        display2 = cv2.cvtColor(depthmap, cv2.COLOR_GRAY2BGR)
                        devmod = np.concatenate((display2, line_seperate), axis=1)
                        # cv2.imshow("Depthmap", depthmap)
                    # if count % 10 == 0:
                    #     self.queue_update_pc.put(const.TYPE_IN)
                    if count > 1:
                        mask, display = backgroundSubtraction.compute(depthmap)
                        # if np.sum(display) > 100:
                        #     print "capture" + str(count)
                        # cv2.imwrite("../capture/back" + str(count) + ".jpg", display)
                        if self.isDevMode == 1:
                            display2 = cv2.cvtColor(display, cv2.COLOR_GRAY2BGR)
                            devmod = np.concatenate((devmod, display2), axis=1)
                            devmod = np.concatenate((devmod, line_seperate), axis=1)
                            # cv2.imshow("Background Subtraction", display)
                        # res,pon1,pon2 = imgObjectMoving.getImgObjectMoving(mask)
                        # if res:
                        #     # cv2.rectangle(display,pon1, pon2,(255,255,255), 2)
                        #     if count>74:
                        #         im_detected = detector.detect(display[pon1[1]:pon2[1],pon1[0]:pon2[0]])
                        #     # cv2.imshow("back", display)
                        #         cv2.imshow("back", im_detected)
                        trackObj.resetTracking()
                        data, data150 = detectMoving.detectObjectInImage(display)
                        # if len(data150) > 0:
                        #     count_y = 0
                        #     for y in data150:
                        #         # print y
                        #         imgx = display[y[0][1]:y[1][1],y[0][0]:y[1][0]]
                        #         cv2.rectangle(image_left,y[0], y[1],(255,255,255), 1)
                        #         # cv2.imwrite("../capture/150/b"+str(count) + str(count_y)+'.jpg', imgx)
                        #         count_y+=1

                        # List center point of objects
                        lstPointObjects = []
                        if len(data) > 0:
                            for x in data:
                                count_y = 0
                                # print x
                                # print x[0], x[1]
                                # print x[1][0] - x[0][0], x[1][1] - x[0][1]
                                # ckObj = trackObj.check_Obj(x[0],x[2])
                                # if ckObj == False:
                                #     cdetect+=1
                                #     print cdetect
                                cv2.circle(image_left, x[3], 25, (255, 255, 255), 1)
                                # cv2.rectangle(image_left, x[0], x[1], (255, 255, 255), 2)
                                # trackObj.trackingObj(x[0], x[2])
                                if detector.detect1(display, x[0], x[1], x[2]):
                                    lstPointObjects.append(x[3])
                                    # trackObj.trackingObj(x[0], x[2], 25)
                                    # cv2.rectangle(image_left,x[0], x[1],(255,255,255), 1)
                                    # else:
                                    # cv2.rectangle(image_left, x[0], x[1], (255, 255, 255), 15)
                                    cv2.circle(image_left, x[3], 25, (255, 255, 255), 3)
                                    y = (detectMoving.CheckRectDetect(x[0], x[1], x[2], 352, 288))
                                    imgx = display[y[0][1]:y[1][1], y[0][0]:y[1][0]]
                                    # cv2.imwrite("../capture/pass/l"+str(count)+str(count_y) + '.jpg', imgx)
                                    # cv2.imwrite("../capture/l"+str(count)+str(count_y) + '.jpg', imgx)

                                    # else:
                                    #     y = (detectMoving.CheckRectDetect(x[0], x[1], x[2], 352, 288))
                                    #     imgx = display[y[0][1]:y[1][1], y[0][0]:y[1][0]]
                                    # cv2.imwrite("../capture/fail/l"+str(count)+str(count_y) + '.jpg', imgx)
                                    # cv2.imwrite("../capture/l"+str(count)+str(count_y) + '.jpg', imgx)
                        if len(lstPointObjects) > 0:
                            trackObj.trackingAllObject(lstPointObjects)
                        trackObj.remove_track()
                        for headpoint in trackObj.allObj:
                            firstpoint = None
                            for point in headpoint.historyPoints:
                                if firstpoint != None:
                                    cv2.line(image_left,firstpoint,point,(255, 255, 255), 1)
                                    firstpoint = point
                                else:
                                    firstpoint = point
                        cv2.line(image_left, (0, 144 - 70), (352, 144 - 70), (255, 255, 255), 1)
                        # cv2.line(image_left, (0, 144), (352, 144), (255, 255, 255), 1)
                        cv2.line(image_left, (0, 144 + 70), (352, 144 + 70), (255, 255, 255), 1)
                        cv2.putText(image_left, 'In: %i' % trackObj.InSh, (160, 20), font, 0.5, (255, 255, 255), 1)
                        cv2.putText(image_left, 'Out: %i' % trackObj.OutSh, (160, 276), font, 0.5, (255, 255, 255), 1)
                        cv2.putText(image_left, 'fps = ' + str(int(1 / (time.time() - t1))), (10, 20), font, 0.5,
                                    (255, 255, 255), 1)
                        if self.isDevMode == 1:
                            devmod = np.concatenate((devmod, image_left), axis=1)
                            cv2.imshow("Develop Mod", devmod)
                        else:
                            cv2.imshow("Camera", image_left)

                    # print "-----------------------------" + str(count)

                    # if res:
                    #     cv2.rectangle(display,pon1, pon2,(255,255,255), 2)
                    # print trackObj.allObj
                    # print 'fps = ' + str(1 / (time.time() - t1))
                    count += 1
                    char = cv2.waitKey(1)

                    if (char == 99):
                        #     count += 1
                        #     cv2.imwrite(str(count)+'.jpg', display)
                        #     video_writer_right.release()
                        #     video_writer_left.release()
                        print trackObj.InSh, trackObj.OutSh

                        cv2.waitKey(0)
                    if (char == 27):
                        break
                except Exception, ex:
                    print 'Thread_Listening_Socket WHILE Exception: ' + str(ex)

        except Exception, ex:
            print 'Thread_Listening_Socket Exception: ' + str(ex)

        self.stop()
