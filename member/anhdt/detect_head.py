__author__ = 'anhdt'
import cv2
import numpy as np

WIDTH_PCONS, HEIGHT_PCONS = [100,100]
WIDTH_HCONS, HEIGHT_HCONS = [50,50]
img = cv2.imread("xx5.jpg")
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
HEIGHT_IMG, WIDTH_IMG = img.shape

def checkHead(img,pon1,pon2):
    if pon2[1] - pon1[1] < WIDTH_HCONS or pon2[0] - pon1[0] < WIDTH_HCONS:
        return False
    return True

def checkPeople(img,pon1,pon2,xindex):
    if pon2[1] - pon1[1] < WIDTH_PCONS or pon2[0] - pon1[0] < HEIGHT_PCONS:
        return False , None
    imgx = img[pon1[1]:pon2[1],pon1[0]:pon2[0]]
    ret, data = cv2.threshold(imgx,0.49*opening.max(),255,cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(data,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    datax = []
    for cn in contours:
        ver = cv2.boundingRect(cn)
        if cv2.contourArea(cn) > 0:
            maiorArea = cv2.contourArea(cn)
            rect = ver
            # print rect
            ponto1 = (rect[0], rect[1])
            ponto2 = (rect[0]+ rect[2],rect[1]+rect[3])
            if checkHead(imgx,ponto1,ponto2):
                print ponto1
                print ponto2
                datax.append([ponto1,ponto2])
                cv2.rectangle(imgx, ponto1, ponto2,(255,255,255), 2)
    # xindex1 = xindex + 1
    # cv2.imshow("xxx %i"%xindex1,data)
    cv2.imshow("xxx %i"%xindex,imgx)
    if len(datax) == 1:
        cv2.imshow("xxx %i"%xindex,imgx)
        return True , datax
    else:
        return False, None

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
opening = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel, iterations = 3)
re,thresh1 = cv2.threshold(opening,80,255,cv2.THRESH_BINARY)
sure_bg = cv2.dilate(thresh1,kernel,iterations=3)
cinza = cv2.erode(sure_bg,kernel,iterations = 3)
# ret, sure_fg = cv2.threshold(sure_bg,0.7*sure_bg.max(),255,0)
# sure_fg = np.uint8(sure_fg)

contours, hierarchy = cv2.findContours(cinza,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# cv2.imshow("opening2",sure_fg)
xindex = 0
for cn in contours:
    ver = cv2.boundingRect(cn)
    if cv2.contourArea(cn) > 0:
        maiorArea = cv2.contourArea(cn)
        rect = ver
        # print rect
        xindex += 1
        ponto1 = (rect[0], rect[1])
        ponto2 = (rect[0]+ rect[2],rect[1]+rect[3])
        ck, data = checkPeople(opening,ponto1,ponto2,xindex)
        if ck:
            # pon1 = (ponto1[0]+data[0][0][0],ponto1[1]+data[0][0][1])
            # pon2 = (ponto2[0]+data[0][1][0],ponto2[1]+data[0][1][1])
            pon1 = (ponto1[0]+data[0][0][0],ponto1[1]+data[0][0][1])
            pon2 = (pon1[0]+data[0][1][0]-data[0][0][0],pon1[1]+data[0][1][1])
            cv2.rectangle(img, pon1, pon2,(255,255,255), 2)
            cv2.rectangle(cinza, pon1, pon2, (255,255,255), 1)
# cv2.imshow("thread",thresh1)
# sure_2 = img[348:361,157:171]
# cv2.imshow("opening1",sure_2)
cv2.imshow("raw",img)
# cv2.imshow("rx",sure_bg)
# cv2.imshow("rx2",cinza)
cv2.waitKey(0)
cv2.destroyAllWindows()