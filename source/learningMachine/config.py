'''
Set the config variable.
'''

# import ConfigParser as cp
# import json
#
# config = cp.RawConfigParser()
# config.read('./config.cfg')

# min_wdw_sz = json.loads(config.get("hog","min_wdw_sz"))
# step_size = json.loads(config.get("hog", "step_size"))
# orientations = config.getint("hog", "orientations")
# pixels_per_cell = json.loads(config.get("hog", "pixels_per_cell"))
# cells_per_block = json.loads(config.get("hog", "cells_per_block"))
# visualize = config.getboolean("hog", "visualize")
# normalize = config.getboolean("hog", "normalize")

# HOG
min_wdw_sz = (150, 150)
step_size = (30, 30)
orientations = 9
pixels_per_cell = (10, 10)
cells_per_block = (2, 2)
visualize = False
normalize = True

# pos_feat_ph = config.get("paths", "pos_feat_ph")
# neg_feat_ph = config.get("paths", "neg_feat_ph")
# model_path = config.get("paths", "model_path")

# path
pos_feat_ph = "../../data/features/pos"
neg_feat_ph = "../../data/features/neg"
model_path = "../data/models/svm.model"
model_train_path = "../../data/models/svm.model"

#nms
threshold = .3

# threshold = config.getfloat("nms", "threshold")