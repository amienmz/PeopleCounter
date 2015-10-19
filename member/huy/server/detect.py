__author__ = 'anhdt'
import cv2
#==================================================#
#====================Detect========================#
#==================================================#

WIDTH_PCONS, HEIGHT_PCONS = [100,100]
WIDTH_HCONS, HEIGHT_HCONS = [50,50]
SIZE_HEAD_MAX, SIZE_HEAD_MIN = [1.08,0.3]
HEIGHT_IMG, WIDTH_IMG = [288,352]
LINE_POS_TOP, LINE_POS_BOT = [144-50, 144+50]

def checkHead(img,pon1,pon2):
    if pon2[1] - pon1[1] < WIDTH_HCONS or pon2[0] - pon1[0] < WIDTH_HCONS:
        return False
    else:
        return True
    # if SIZE_HEAD_MIN < (pon2[1]*1.0)/(pon2[0]*1.0) < SIZE_HEAD_MAX:
    #     return True
    # else:
    #     return False

def checkHumanWithHead(data,w_b,h_b):
    nhyHead = len(data)
    if nhyHead == 1:
        lfx=data[0][0][0]
        rgx=w_b-data[0][1][0]-lfx
        if rgx < data[0][1][0] and lfx < data[0][1][0]:
            return True
        else:
            return False
    elif nhyHead > 1:
        return True
    else:
        return False

def checkPeople(img,pon1,pon2,xindex):
    if pon2[1] - pon1[1] < WIDTH_PCONS or pon2[0] - pon1[0] < HEIGHT_PCONS:
        return False , None
    imgx = img[pon1[1]:pon2[1],pon1[0]:pon2[0]]
    wx,hx = imgx.shape
    ret, data = cv2.threshold(imgx,imgx.mean()+40,imgx.max(),cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(data,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    datax = []
    for cn in contours:
        ver = cv2.boundingRect(cn)
        if cv2.contourArea(cn) > 300:
            maiorArea = cv2.contourArea(cn)
            rect = ver
            # print rect
            ponto1 = (rect[0], rect[1])
            ponto2 = (rect[0]+ rect[2],rect[1]+rect[3])
            if checkHead(imgx,ponto1,ponto2):
                datax.append([ponto1,ponto2])
            # ponx1 = (pon1[0]+ponto1[0],pon1[1]+ponto1[1])
            # ponx2 = (ponx1[0]+ponto2[0]-ponto1[0],pon1[1]+ponto2[1])
            # cv2.rectangle(img, ponx1, ponx2,(255,255,255), 2)
    # checkHumanWithHead(datax,pon2[0],pon2[1])
    # cv2.imshow("xxx %i"%xindex,imgx)
    # cv2.imshow("xxx %i"%xindex,imgx)
    if checkHumanWithHead(datax,wx,hx):
        # cv2.imshow("xxx %i"%xindex,imgx)
        return True , datax
    else:
        return False, None
    # return False, None

def locRec(pon1,pon2):
    if pon2[1] - pon1[1] < WIDTH_HCONS or pon2[0] - pon1[0] < WIDTH_HCONS:
        return False
    else:
        return True

#==================================================#
#===================End Detect=====================#
#==================================================#