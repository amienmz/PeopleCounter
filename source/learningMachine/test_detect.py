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

im = cv2.imread("../../data/dataset/neg/crop382.jpg", 0)

clf = joblib.load(model_train_path)
fd, hogimage = hog(im, orientations, pixels_per_cell, cells_per_block, True)#, normalize)
cv2.imwrite("hog.jpg", hogimage)
print len(fd)
print clf.predict(fd)


