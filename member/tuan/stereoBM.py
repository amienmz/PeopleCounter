__author__ = 'pc'
import numpy as np
import cv2
from matplotlib import pyplot as plt
def nothing(x):
    pass

video1 = cv2.VideoCapture(0)
video1.set(3,400)
video1.set(4,300)

video2 = cv2.VideoCapture(1)
video2.set(3,400)
video2.set(4,300)

# imgL = cv2.imread('images/im2.png',0)
# imgR = cv2.imread('images/im6.png',0)
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
NumDis = 16

# calibration camera

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# for fname in images:
img = cv2.imread('L.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# cv2.imshow("s", gray)
# cv2.waitKey(0)
# Find the chess board corners
ret, corners = cv2.findChessboardCorners(gray, (7,7),None)

# If found, add object points, image points (after refining them)
if ret == True:
    print "trueee"
    objpoints.append(objp)

    corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
    imgpoints.append(corners2)

    # Draw and display the corners
    # img = cv2.drawChessboardCorners(img, (6,8), corners2,ret)
    # cv2.imshow('img',img)
    # cv2.waitKey(500)

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
    img = cv2.imread('L.png')
    h,  w = img.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

while(1):
    ret1, frame1 = video1.read()
    ret2, frame2 = video2.read()

    frameR = cv2.cvtColor(frame1,cv2.COLOR_RGB2GRAY)
    frameL = cv2.cvtColor(frame2,cv2.COLOR_RGB2GRAY)

    # calibrate image Left
    imgL = cv2.undistort(frameL, mtx, dist, None, newcameramtx)
    # crop the image
    x,y,w,h = roi
    imgL = imgL[y:y+h, x:x+w]

    # calibrate image right
    imgR = cv2.undistort(frameR, mtx, dist, None, newcameramtx)
    # crop the image
    x,y,w,h = roi
    imgR = imgR[y:y+h, x:x+w]

    # imgL = cv2.imread("images/imageL.png", 0)
    # imgR = cv2.imread("images/imageR.png", 0)

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
    cv2.imshow("R", imgR)
    cv2.imshow("L", imgL)
    # cv2.fastNlMeansDenoising(imgR,None,3,7,21)
    # cv2.imshow("2", imgR)
    char = cv2.waitKey(1)
    if (char == 27):
        break

cv2.destroyAllWindows()
# np.savetxt("ar.txt",disparity)
# plt.imshow(disparity,'gray')
# plt.show()