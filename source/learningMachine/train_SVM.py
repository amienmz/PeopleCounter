# Import the required modules
from skimage.feature import local_binary_pattern
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
import argparse as ap
import numpy as np
import glob
import os
from config import *

if __name__ == "__main__":
     #detete old data before train
    os.system("rm -rf /home/pc/PycharmProjects/PeopleCounter/data/models/*")

    pos_feat_path = "../../data/features/pos"
    neg_feat_path = "../../data/features/pos"

    # Classifiers supported
    clf_type = "LIN_SVM"

    fds = []
    # fds = np.array([])
    labels = []
    # Load the positive features
    for feat_path in glob.glob(os.path.join(pos_feat_path,"*.feat")):
        fd = joblib.load(feat_path)
        print len(fd)
        if len(fd) == 7056:
            fds.append(fd)
            labels.append(1)

    # Load the negative features
    for feat_path in glob.glob(os.path.join(neg_feat_path,"*.feat")):
        fd = joblib.load(feat_path)
        if len(fd) == 7056:
            fds.append(fd)
            labels.append(-1)

    # print fds
    if clf_type is "LIN_SVM":
        clf = LinearSVC()
        print "Training a Linear SVM Classifier"
        clf.fit(fds, labels)
        # If feature directories don't exist, create them
        if not os.path.isdir(os.path.split(model_train_path)[0]):
            os.makedirs(os.path.split(model_train_path)[0])
        joblib.dump(clf, model_train_path)
        print "Classifier saved to {}".format(model_train_path)