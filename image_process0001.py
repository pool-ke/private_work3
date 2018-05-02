#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 16:09:12 2017

@author: root
"""

import cv2 as cv
from PIL import ImageEnhance
import matplotlib.pyplot as plt
import numpy as np

def fun_CONTRAST(img):
    en_2 = ImageEnhance.Contrast(img)
    contrast = 1.5
    img_temp = en_2.enhance(contrast)
    print(22)
    return img_temp
#file_path="Figure_1.png"
file_path="/home/huawei/myfile/code_python/KE/ROI_Logo/H/OK/M-NG26_0.png"
img1=cv.imread(file_path)

a=range(50,100)
for i in range(50,100):
    print (i)
#img2=cv.GaussianBlur(img1,(5,5),1)
#img3=cv.Canny(img2,90,100)
#print (img1)
#print (img1.shape)
img2=img1
#
#for i in range(100):
#    for j in range(50):
#        img2[i][j][0]=255
#        img2[i][j][1]=0
#        img2[i][j][2]=0
print(img2)
print(img2.shape)


a=range(int(350-radius),int(350+radius))
b=range(int(350-radius),int(350+radius))
        for i in a:
            for j in b:
                img_temp[i][j][0]=255
                img_temp[i][j][1]=0
                img_temp[i][j][2]=0

print(img2)
print(img2.shape)

plt.figure()
plt.subplot(121)
plt.imshow(img1)
plt.subplot(122)
plt.imshow(img2)
plt.show()


