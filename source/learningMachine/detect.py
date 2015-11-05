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
        self.count = 0


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
                # print  "Detection:: Location -> ({}, {})".format(x, y)
                # print "Scale ->  {} | Confidence Score {} \n".format(scale,self.clf.decision_function(fd))
                # print "%.9f" % (self.clf.decision_function(fd))
                detections.append((x, y, self.clf.decision_function(fd),
                    int(self.min_wdw_sz[0]),
                    int(self.min_wdw_sz[1])))
                # cd.append(detections[-1])


        # Display the results before performing NMS
        clone = image.copy()

        detections = nms(detections, threshold)

        # Display the results after performing NMS
        for (x_tl, y_tl, decision, w, h) in detections:
            # Draw the detections
            if decision > 0.5:
                cv2.rectangle(clone, (x_tl, y_tl), (x_tl+w,y_tl+h), (255, 255, 0), thickness=3)
            else:
                cv2.rectangle(clone, (x_tl, y_tl), (x_tl+w,y_tl+h), (255, 255, 0), thickness=1)
            crop_image = image[y_tl: y_tl+h, x_tl: x_tl+w]
            cv2.imwrite("capture/crop" + str(self.count) + ".jpg", crop_image)
            self.count+=1
        return clone
