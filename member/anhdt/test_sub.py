__author__ = 'anhdt'
import cv2

cam = cv2.VideoCapture(0)

ret, bg = cam.read()
bg = cv2.medianBlur(bg,5)
while True:
    ret, frame = cam.read()
    # frame = cv2.blur(frame, (5,5))
    # frame = cv2.bilateralFilter(frame,5,75,75)
    frame = cv2.medianBlur(frame,5)
    mask = frame - bg

    gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    ret, gray = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    # gray = cv2.dilate(gray,None,iterations=3)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)

    gray = cv2.medianBlur(gray,5)
    # gray = cv2.blur(gray, (9,9))
    # gray = cv2.bilateralFilter(gray,5,75,75)
    res = cv2.bitwise_and(frame,frame,None,gray)
    #cv2.imshow("mask", mask)
    cv2.imshow("gray", gray)
    cv2.imshow("webcam", frame)
    cv2.imshow("mask",mask)
    cv2.imshow("res",res)
    if cv2.waitKey(2) & 0xFF == 27:
        break

cam.release()
cv2.destroyAllWindows()