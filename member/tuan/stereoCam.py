__author__ = 'pc'
import cv2


video1 = cv2.VideoCapture(0)
video1.set(3,640)
video1.set(4,480)
saveVideoL = cv2.VideoWriter("videoL.mpg",-1, 10, (640,480))


video2 = cv2.VideoCapture(2)
video2.set(3,640)
video2.set(4,480)
saveVideoR = cv2.VideoWriter("videoR.mpg",-1, 10, (640,480))

loop = True
while(loop == True):
    ret1, frame1 = video1.read()
    ret2, frame2 = video2.read()

    saveVideoL.write(frame1)
    saveVideoR.write(frame2)

    cv2.imshow("video1", frame1)
    cv2.imshow("video2", frame2)

    char = cv2.waitKey(99)
    if (char == 99):
        # cv2.imwrite("R.png", frame1)
        # cv2.imwrite("L.png", frame2)
        loop = False

video1.release()
video2.release()

cv2.destroyAllWindows()