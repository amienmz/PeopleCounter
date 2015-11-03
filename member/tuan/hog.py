__author__ = 'pc'
from skimage.feature import hog
from skimage.io import imread
from sklearn.externals import joblib
# To read file names
import argparse as ap
import glob
import cv2
import numpy as np
import os

min_wdw_sz = (150, 150)
step_size = (30, 30)
orientations = 9
pixels_per_cell = (10, 10)
cells_per_block = (2, 2)
visualize = True
normalize = True

path = "../../data/dataset/pos/pos-358.jpg"

im = cv2.imread(path, 0)
im = cv2.Canny(im,100,100)
cv2.imshow("image", im)
cv2.waitKey(0)
fd, hogimage = hog(im, orientations, pixels_per_cell, cells_per_block, visualize, normalize)
cv2.imshow("hog", hogimage)
print fd
np.savetxt("hog.txt", fd,fmt='%f' ,delimiter=' ')
cv2.imwrite("hog.jpg", hogimage)
cv2.imwrite("im.jpg", im)
