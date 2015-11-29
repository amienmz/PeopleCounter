__author__ = 'pc'
from skimage.feature import hog
from skimage.io import imread
from sklearn.externals import joblib
# To read file names
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
import argparse as ap
import glob
import cv2
import numpy as np
import os

min_wdw_sz = (150, 150)
step_size = (10, 10)
orientations = 8
pixels_per_cell = (15, 15)
cells_per_block = (1, 1)
visualize = True
normalize = True

path_pos = "../../data/dataset/pos/pos-15.png"
# path_pos = "test.png"
path_neg1 = "../../data/dataset/neg/neg-16.png"
path_neg2 = "../../data/dataset/neg/neg-18.png"
path_test = "../../data/dataset/neg/neg-66.png"
# path_test = "../../data/dataset/pos/pos-16.png"

im_pos = cv2.imread("l1210.jpg", 0)
# im_pos = cv2.Canny(im_pos,100,100)

# im_neg1 = cv2.imread(path_neg1, 0)
# im_neg2 = cv2.imread(path_neg2, 0)
# im_neg = cv2.Canny(im_neg, 100, 100)
# fd1, hogimage1 = hog(im_pos, orientations=8, pixels_per_cell=(16, 16),cells_per_block=(1, 1), visualise=True)
fd1, image = hog(im_pos, orientations, pixels_per_cell, cells_per_block, visualize)
cv2.imshow("s", image)
cv2.waitKey(0)
cv2.imwrite("hog_out.jpg", image)
# fd2 = hog(im_neg1, orientations, pixels_per_cell, cells_per_block, visualize)
# fd3 = hog(im_neg2, orientations, pixels_per_cell, cells_per_block, visualize)
#
# X = []
# y = []
#
# X.append(fd1)
# X.append(fd2)
# X.append(fd3)
#
# y.append(1)
# y.append(0)
# y.append(0)
# X = [fd1, fd2, fd3]
# y = [1, 0, 0]
#
# clf = LinearSVC()
# clf.fit(X,y)

# im_test = cv2.imread(path_test, 0)
# im_test = cv2.Canny(im_test,100,100)
# fd4 = hog(im_test, orientations, pixels_per_cell, cells_per_block, visualize)
#
# print clf.predict(fd4)
# print clf.score(fd3,[0])
# print clf.decision_function(fd3)

#
# np.savetxt("hog.txt", fd1, fmt='%f' ,delimiter=' ')
# cv2.imwrite("hog.jpg", hogimage1)
# cv2.imwrite("im.jpg", im_pos)
