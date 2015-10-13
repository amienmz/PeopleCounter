__author__ = 'huybu'
import cv2
import cv
# find the webcam
CAM_RIGHT=1
CAM_LEFT=2
capture_right = cv2.VideoCapture(CAM_RIGHT)
capture_right.set(3,352)
capture_right.set(4,288)

capture_left = cv2.VideoCapture(CAM_LEFT)
capture_left.set(3,352)
capture_left.set(4,288)
CODEC = cv.CV_FOURCC('M','P','4','V') # MPEG-4 = MPEG-1
# video recorder
video_writer_right = cv2.VideoWriter("outputR24.avi", -1, 24, (352, 288))

video_writer_left = cv2.VideoWriter("outputL24.avi", -1, 24, (352, 288))

# record video
while True:
    ret, frameR = capture_right.read()

    video_writer_right.write(frameR)
    cv2.imshow('Video Stream Right', frameR)


    ret, frameL = capture_left.read()

    video_writer_left.write(frameL)
    cv2.imshow('Video Stream Left', frameL)

    char = cv2.waitKey(1)
    if (char == 27):
        break


video_writer_right.release()
video_writer_left.release()
capture_right.release()
capture_left.release()
cv2.destroyAllWindows()