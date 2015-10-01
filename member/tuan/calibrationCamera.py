import numpy as np
import cv2
import glob

CHESS_ROW = 5
CHESS_COL = 5

video1 = cv2.VideoCapture(0)
video1.set(3,400)
video1.set(4,300)

video2 = cv2.VideoCapture(1)
video2.set(3,400)
video2.set(4,300)

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# images = glob.glob('*.jpg')

while(True):
    ret1, frame1 = video1.read()
    ret2, frame2 = video2.read()
    if ret1 == True and ret2 == True:
        frameR = cv2.cvtColor(frame1,cv2.COLOR_RGB2GRAY)
        frameL = cv2.cvtColor(frame2,cv2.COLOR_RGB2GRAY)

        cv2.imshow("R", frameR)
        cv2.imshow("L", frameL)
        char = cv2.waitKey(1)
        if (char == 99):

            # Find the chess board corners
            retR, cornersR = cv2.findChessboardCorners(frameR, (CHESS_ROW,CHESS_COL),None)
            retL, cornersL = cv2.findChessboardCorners(frameL, (CHESS_ROW,CHESS_COL),None)

            # If found, add object points, image points (after refining them)
            if retR == True and retL == True:

                objpoints.append(objp)

                corners2R = cv2.cornerSubPix(frameR,cornersR,(11,11),(-1,-1),criteria)
                imgpoints.append(corners2R)

                corners2L = cv2.cornerSubPix(frameL,cornersL,(11,11),(-1,-1),criteria)
                imgpoints.append(corners2L)

                # Draw and display the corners
                imgR = cv2.drawChessboardCorners(imgR, (CHESS_ROW,CHESS_COL), corners2R,retR)
                cv2.imshow('imgR',imgR)

                imgL = cv2.drawChessboardCorners(imgL, (CHESS_ROW,CHESS_COL), corners2L,retL)
                cv2.imshow('imgL',imgL)

                char = cv2.waitKey(1)
                if (char == 27):
                    break

cv2.destroyAllWindows()