__author__ = 'pc'
# Import the required modules
from skimage.transform import pyramid_gaussian
from skimage.io import imread
from skimage.feature import hog
from sklearn.externals import joblib
import cv2
import argparse as ap
from nms import nms
from config import *

class Detector(object):
    def __init__(self, min_window_size, step_size, downscale):
        self.min_wdw_sz = min_window_size
        self.step_size = step_size
        self.downscale = downscale
        self.clf = joblib.load(model_path)
        self.sizeImg = 150

    def sliding_window(self, image, window_size, step_size):
        '''
        This function returns a patch of the input image `image` of size equal
        to `window_size`. The first image returned top-left co-ordinates (0, 0)
        and are increment in both x and y directions by the `step_size` supplied.
        So, the input parameters are -
        * `image` - Input Image
        * `window_size` - Size of Sliding Window
        * `step_size` - Incremented Size of Window

        The function returns a tuple -
        (x, y, im_window)
        where
        * x is the top-left x co-ordinate
        * y is the top-left y co-ordinate
        * im_window is the sliding window image
        '''
        for y in xrange(0, image.shape[0], step_size[1]):
            for x in xrange(0, image.shape[1], step_size[0]):
                yield (x, y, image[y:y + window_size[1], x:x + window_size[0]])

    def detect(self,image):
        # image = cv2.Canny(image,100,100)
        # Load the classifier

        # List to store the detections
        detections = []
        # The current scale of the image
        scale = 0
        # Downscale the image and iterate

        # This list contains detections at the current scale
        cd = []
        # If the width or height of the scaled image is less than
        # the width or height of the window, then end the iterations.
        for (x, y, im_window) in self.sliding_window(image, self.min_wdw_sz, self.step_size):
            if im_window.shape[0] != self.min_wdw_sz[1] or im_window.shape[1] != self.min_wdw_sz[0]:
                continue
            # Calculate the HOG features
            fd = hog(im_window, orientations, pixels_per_cell, cells_per_block, visualize)#, normalize)
            pred = self.clf.predict(fd)
            # print "predict: " + str(pred)
            if pred == 1:
                print  "Detection:: Location -> ({}, {})".format(x, y)
                print "Scale ->  {} | Confidence Score {} \n".format(scale,self.clf.decision_function(fd))
                print "%.9f" % (self.clf.decision_function(fd))
                detections.append((x, y, self.clf.decision_function(fd),
                    int(self.min_wdw_sz[0]),
                    int(self.min_wdw_sz[1])))
                # cd.append(detections[-1])


        # Display the results before performing NMS
        clone = image.copy()

        detections = nms(detections, threshold)

        # Display the results after performing NMS
        for (x_tl, y_tl, _, w, h) in detections:
            # Draw the detections
            cv2.rectangle(clone, (x_tl, y_tl), (x_tl+w,y_tl+h), (255, 255, 0), thickness=2)
        return clone

    def CheckRectDetect(self,pon1,pon2,pon3,w,h):
        datah = self.sizeImg - pon3[1]
        dataw = self.sizeImg - pon3[0]
        if datah % 2 != 0:
            data11= int(datah/2)
            data21 = data11 + 1
        else:
            data21 =data11 = int(datah/2)
        if dataw % 2 != 0:
            data10= int(dataw/2)
            data20 = data10 + 1
        else:
            data20 =data10= int(dataw/2)

        if pon1[0]-data10 < 0:
            data20 += (data10 - pon1[0])
            data10 = pon1[0]
        if pon1[1]-data11 < 0:
            data21 += (data11 - pon1[1])
            data11 = pon1[1]
        # print pon1,pon2
        if pon2[0]+data20 >= w:
            data10 += (data20 - (w - pon2[0]))
            data20 = (w - pon2[0])
        if pon2[1]+data21 >= h:
            data11 += (data21 - (h - pon2[1]))
            data21 = (h - pon2[1])
        return (pon1[0]-data10,pon1[1]-data11),(pon2[0]+data20,pon2[1]+data21)

    def detect1(self,image,pon1,pon2,pon3):
        # image = cv2.Canny(image,100,100)
        # Load the classifier
        h,w = image.shape
        IsHead = False;
        # List to store the detections
        datax,datay = self.CheckRectDetect(pon1,pon2,pon3,w,h)
            # Calculate the HOG features
        im_window = image[datax[1]:datay[1],datax[0]:datay[0]]
        fd = hog(im_window, orientations, pixels_per_cell, cells_per_block, visualize)#, normalize)
        pred = self.clf.predict(fd)
        # print "predict: " + str(pred)
        if pred == 1:
            IsHead = True

        return IsHead