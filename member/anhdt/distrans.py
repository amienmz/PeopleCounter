from __future__ import print_function

import numpy as np
import cv2
from common import make_cmap

if __name__ == '__main__':
    import sys
    fn ="955.jpg"

    img = cv2.imread(fn, 0)
    if img is None:
        print('Failed to load fn:', fn)
        sys.exit(1)

    need_update = True
    voronoi = False

    def update(dummy=None):
        global need_update
        need_update = False
        thrs = cv2.getTrackbarPos('threshold', 'distrans')
        mark = cv2.Canny(img, thrs, 3*thrs)
        dist, labels = cv2.distanceTransformWithLabels(~mark, cv2.cv.CV_DIST_L2, 5)
        if voronoi:
            vis = cm[np.uint8(labels)]
        else:
            vis = cm[np.uint8(dist*2)]
        vis[mark != 0] = 255
        cv2.imshow('distrans', vis)

    def invalidate(dummy=None):
        global need_update
        need_update = True

    cv2.namedWindow('distrans')
    cv2.createTrackbar('threshold', 'distrans', 60, 255, invalidate)
    update()


    while True:
        ch = 0xFF & cv2.waitKey(50)
        if ch == 27:
            break
        if ch == ord('v'):
            voronoi = not voronoi
            print('showing', ['distance', 'voronoi'][voronoi])
            update()
        if need_update:
            update()
    cv2.destroyAllWindows()