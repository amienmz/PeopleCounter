__author__ = 'anhdt'
#======================================#
#==============Tracking================#
#======================================#
allObj = []
InSh = 0
OutSh = 0
def resetTracking():
    for data in allObj:
        data[4] = False
    return None

def remove_track():
    for data in allObj:
        if data[4] == False:
            data[0] = None
            data[1] = None
            data[2] = None
            data[3] = None
            data[5] = 0
            data[6] = 0
    return None

def check_in_out(data):
    #0: out
    #1: in
    #-1: unknow
    if data[5] > 0  and data[6] > 0:
        if data[5] >  data[6]:
            data[5] = 0
            data[6] = 0
            return 1
        else:
            data[5] = 0
            data[6] = 0
            return 0
    else:
        return -1
def sysn_line(data,y,h):
    ln = check_withLine(y,h)
    if ln < 0:
        return False
    if data[5] == 0 or data[5] == ln:
        data[5] = ln
    elif data[6] == 0 or data[6] == ln:
        data[6] = ln
    return True
def check_withLine(y,h):
    if y <= LINE_POS_TOP <= y+h:
        return 1
    elif y <= LINE_POS_BOT <= y+h:
        return 2
    else:
        return -1

def check_nextline(pon1,pon2):
    global InSh , OutSh
    y, x = [pon1[1],pon1[0]]
    h, w = [pon2[1],pon2[0]]
    # print x,y,w,h
    if len(allObj) == 0:
        allObj.append([x,y,w,h,True,0,0])
        return None
    haveline = False
    for data in allObj:
        if data[0] != None:
            if (data[1] <= y <= data[1]+data[3] and x <= data[0] <= x + w) or (x<=data[0]<=x+w and y <= data[1]<=y+h)or (data[0] <= x <= data[0] + data[2] and y<=data[1]<=y+h) or (data[0] <= x <= data[0]+data[2] and data[1]<=y<=data[1]+data[3]):
                # Point1 = ((data[0]+data[2])/2,(data[1]+data[3])/2)
                data[0] = x
                data[1] = y
                data[2] = w
                data[3] = h
                data[4] = True
                if sysn_line(data,y,h) == False:
                    inout = check_in_out(data)
                    if inout == 0:
                        OutSh +=1
                    elif inout == 1:
                        InSh +=1
                # Point2 = ((data[0]+data[2])/2,(data[1]+data[3])/2)
                # cv2.line(img,Point1,Point2,(255,255,255),1)
                # ins = allObj.index(data)
                # allObj.insert(ins,[x,y,w,h,True])
                # allObj.remove(x)
                haveline = True
                break
    if haveline == False:
        try:
            ins = allObj.index([None,None,None,None,False,0,0])
            allObj.insert(ins,[x,y,w,h,True,0,0])
            allObj.remove(allObj[ins+1])
        except Exception as e:
            allObj.append([x,y,w,h,True,0,0])
    return None
#======================================#
#============End Tracking==============#
#======================================#