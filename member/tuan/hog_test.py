import matplotlib.pyplot as plt

from skimage.feature import hog
from skimage import data, color, exposure
import numpy as np
import cv2

image = np.array([[100,0,0],[100,100,0],[100,100,100]], np.uint8)
print image


# image = cv2.imread("../../data/dataset/pos/pos-15.png", 0)
#
# fd, hog_image = hog(image, orientations=8, pixels_per_cell=(16, 16),
#                     cells_per_block=(1, 1), visualise=True)
hog_image = hog(image, orientations=9, pixels_per_cell=(3, 3),
                    cells_per_block=(1, 1), visualise=False)
print hog_image
print 5 / 10
# cv2.imwrite("test.jpg", hog_image)
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), sharex=True, sharey=True)
#
# ax1.axis('off')
# ax1.imshow(image, cmap=plt.cm.gray)
# ax1.set_title('Input image')
# ax1.set_adjustable('box-forced')
#
# # Rescale histogram for better display
# hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 0.02))
#
# ax2.axis('off')
# ax2.imshow(hog_image_rescaled, cmap=plt.cm.gray)
# ax2.set_title('Histogram of Oriented Gradients')
# ax1.set_adjustable('box-forced')
# plt.show()

# im = cv2.imread("hog.jpg",0)
# print np.sum(im)