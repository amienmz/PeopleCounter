import cv2
import numpy as np



image = cv2.imread("head5.png", 0)
num_of_drop = 10

maxValue = 256
m_a = None
m_b = None
m_c = None

locX = 0
locY = 0

minP = maxValue
imgHeight, imgWidth = image.shape[:2]

output = np.zeros(image.shape, dtype=int)

label_P = []

m_d = None

inputcopy = image.copy()
m_a = image.copy()
m_b = image.copy()

index = 0
for i in range(imgWidth*imgHeight):
    if()


