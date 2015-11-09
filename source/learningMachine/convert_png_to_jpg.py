# Import the functions to calculate feature descriptors
from skimage.feature import local_binary_pattern
from skimage.feature import hog
from skimage.io import imread
from sklearn.externals import joblib
# To read file names
import argparse as ap
import glob
import cv2
import os
from config import *

if __name__ == "__main__":
    pos_im_path = "../../data/dataset/pos"
    neg_im_path = "../../data/dataset/neg"
	


    # If feature directories don't exist, create them
    if not os.path.isdir(pos_feat_ph):
        os.makedirs(pos_feat_ph)

    # If feature directories don't exist, create them
    if not os.path.isdir(neg_feat_ph):
        os.makedirs(neg_feat_ph)

    print "Converting positive image"
    for im_path in glob.glob(os.path.join(pos_im_path, "*")):
        im = cv2.imread(im_path)
        newpath = im_path[:-3] + "jpg"
        # print newpath
        cv2.imwrite(newpath, im)

    print "Converting negative image"
    for im_path in glob.glob(os.path.join(neg_im_path, "*")):
        im = cv2.imread(im_path)
        newpath = im_path[:-3] + "jpg"
        cv2.imwrite(newpath, im)
        # print newpath