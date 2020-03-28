import cv2 
import numpy as np
import matplotlib.pyplot as plt

import sys
lowThres=int(sys.argv[1])
print(lowThres)
# read the image
image = cv2.imread("img/1.jpg")

# convert it to grayscale
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)



thres = lowThres*3
_frame=gray
edges = cv2.Canny(_frame, threshold1=lowThres, threshold2=thres)
height = gray.shape[0]
width = gray.shape[1]
for y in range(height):
    for x in range(width):
        if(edges[y][x]==255):
            _frame[y][x]=255
cv2.imshow("threshold",_frame)
cv2.waitKey(0)

