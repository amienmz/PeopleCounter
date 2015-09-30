__author__ = 'pc'
import numpy as np
import cv2
from matplotlib import pyplot as plt
def nothing(x):
    pass
imgL = cv2.imread('images/left.jpg',0)
imgR = cv2.imread('images/right.jpg',0)
# imgL = cv2.imread('images/imageL.png',0)
# imgR = cv2.imread('images/imageR.png',0)
cv2.namedWindow('image')
cv2.createTrackbar('PreFilterCap','image',1,63,nothing)
cv2.createTrackbar('PreFilterSize','image',5,255,nothing)
cv2.createTrackbar('PreFilterType','image',0,1,nothing)
cv2.createTrackbar('SmallerBlockSize','image',0,255,nothing)
cv2.createTrackbar('Disp12MaxDiff','image',0,255,nothing)
cv2.createTrackbar('MinDisparity','image',0,400,nothing)
cv2.createTrackbar('NumDisparities','image',0,20,nothing)
cv2.createTrackbar('SpeckleRange','image',0,3,nothing)
cv2.createTrackbar('SpeckleWindowSize','image',0,5000,nothing)
cv2.createTrackbar('TextureThreshold','image',0,2000,nothing)
cv2.createTrackbar('UniquenessRatio','image',0,30,nothing)
stereo = cv2.StereoBM_create(numDisparities=16, blockSize=25)
stereo.setDisp12MaxDiff(0)
stereo.setPreFilterCap(61)
stereo.setPreFilterSize(5)
stereo.setSmallerBlockSize(0)
stereo.setPreFilterType(1)
stereo.setMinDisparity(-39)
stereo.setNumDisparities(112)
stereo.setSpeckleRange(8)
stereo.setSpeckleWindowSize(0)
stereo.setTextureThreshold (507)
stereo.setUniquenessRatio(0)
disparity = stereo.compute(imgL,imgR,cv2.CV_8U)
disparity_visual = cv2.normalize(disparity,disparity, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
NumDis = 16
PreFilterCap_Raw=0
PreFilterType_Raw=0
PreFilterSize_Raw=0
MinDisparity_Raw=0
SmallerBlockSize_Raw=0
Disp12MaxDiff_Raw=0
NumDisparities_Raw=0
SpeckleRange_Raw=0
SpeckleWindowSize_Raw=0
TextureThreshold_Raw=0
UniquenessRatio_Raw=0
while(500):
    PreFilterCap = cv2.getTrackbarPos('PreFilterCap','image')
    if PreFilterCap <= 0:
        PreFilterCap = 1
    PreFilterType = cv2.getTrackbarPos('PreFilterType','image')
    PreFilterSize = cv2.getTrackbarPos('PreFilterSize','image')
    if PreFilterSize % 2 == 0:
        PreFilterSize+=1
    if PreFilterSize <= 5:
        PreFilterSize = 5
    MinDisparity = cv2.getTrackbarPos('MinDisparity','image')
    MinDisparity -= 300
    SmallerBlockSize = cv2.getTrackbarPos('SmallerBlockSize','image')
    Disp12MaxDiff = cv2.getTrackbarPos('Disp12MaxDiff','image')
    NumDisparities = cv2.getTrackbarPos('NumDisparities','image')
    if NumDisparities > 0:
        NumDis = NumDisparities*16
    SpeckleRange = cv2.getTrackbarPos('SpeckleRange','image')
    SpeckleWindowSize = cv2.getTrackbarPos('SpeckleWindowSize','image')
    TextureThreshold = cv2.getTrackbarPos('TextureThreshold','image')
    UniquenessRatio = cv2.getTrackbarPos('UniquenessRatio','image')

    if PreFilterCap_Raw == PreFilterCap and PreFilterType_Raw == PreFilterType and PreFilterSize_Raw == PreFilterSize and MinDisparity_Raw == MinDisparity and SmallerBlockSize_Raw == SmallerBlockSize and Disp12MaxDiff_Raw == Disp12MaxDiff and NumDisparities_Raw == NumDisparities and SpeckleRange_Raw == SpeckleRange and SpeckleWindowSize_Raw == SpeckleWindowSize and TextureThreshold_Raw == TextureThreshold and UniquenessRatio_Raw == UniquenessRatio:
        continue

    stereo.setPreFilterCap(PreFilterCap)
    stereo.setPreFilterSize(PreFilterSize)
    stereo.setPreFilterType(PreFilterType)
    stereo.setSmallerBlockSize(SmallerBlockSize)
    stereo.setDisp12MaxDiff(Disp12MaxDiff)
    stereo.setMinDisparity(MinDisparity)
    stereo.setNumDisparities(NumDis)
    stereo.setSpeckleRange(SpeckleRange)
    stereo.setSpeckleWindowSize(SpeckleWindowSize)
    stereo.setTextureThreshold (TextureThreshold)
    stereo.setUniquenessRatio(UniquenessRatio)
    disparity = stereo.compute(imgL,imgR,cv2.CV_8U)
    disparity_visual = cv2.normalize(disparity,disparity, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    cv2.imshow("ima",disparity_visual)
    char = cv2.waitKey(1)
    if (char == 27):
        break

cv2.destroyAllWindows()
# np.savetxt("ar.txt",disparity)
# plt.imshow(disparity,'gray')
# plt.show()