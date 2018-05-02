#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 14:34:12 2017

@author: root
"""

import skimage
import skimage.morphology as sm
from skimage import filters
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
file_path="/home/huawei/myfile/code_python/KE/ROI_Logo/H/NG/H_NG3000002_0.png"

def binary_iamg(img_org):
#        print(img_org.shape)
    w_image = img_org.shape[0]
    H_image = img_org.shape[1]
#        a = img_org[1,:,:,0].reshape([w_image,H_image])
#        print(a.shape)
            
#    img =skimage.filters.gaussian(img_org[k,:,:,0].reshape([w_image,H_image]),sigma = 0.4)
#            print(img.shape)
    img_arr = np.array(img_org)

    #img_binary = img.convert("1")
           
    img_binary = filters.threshold_otsu(img_arr)
    print (img_binary)
    for i in range(w_image):
        for j in range(H_image):
            if(img_arr[i,j] <= img_binary):
                img_arr[i,j] = 0
            else:
                img_arr[i,j] = 255
           
#            print(dst2.shape).reshape([w_image,H_image])
    img_arr = sm.opening(img_arr,sm.square(3))
    return img_arr
#image_ori=np.loadtxt("image_org.txt")
#image_out=np.loadtxt("image_out.txt")
#image_out=image_out*255
#cv.imwrite("photo002.png",image_out)

#image_ori1=image_ori*255
image_ori1=cv.imread(file_path)
image_ori2=cv.imread("photo002.png")
image_ori3=cv.imread(file_path)
print (image_ori1.shape)
print (image_ori2.shape)
img1=image_ori1[:,:,0]
img2=image_ori2[:,:,0]
img3=image_ori3[:,:,0]
img4=binary_iamg(img1)
img5=binary_iamg(img2)
img6=img4-img5
#img7 = sm.erosion(img6,sm.square(3))
img7=sm.opening(img6,sm.square(5))
height1=img7.shape[0]
width1=img7.shape[1]
#
count=0
for i in range(height1):
    for j in range(width1):
        if img7[i,j]!=0:
            print (i,j)
            image_ori1[i][j][0]=0
            image_ori1[i][j][1]=255
            image_ori1[i][j][2]=0
            count+=1
#print (img4)
#print (img5)
#print (image_ori1)
#print (image_ori2)
#print (image_ori.shape)
#print (image_out)
#print (image_out.shape)

print (count)
plt.figure()
plt.subplot(141)
#plt.imshow(image_ori1,plt.cm.gray)
plt.imshow(img4,plt.cm.gray)
plt.subplot(142)
#plt.imshow(image_ori2,plt.cm.gray)
plt.imshow(img5,plt.cm.gray)
plt.subplot(143)
plt.imshow(img7,plt.cm.gray)
plt.subplot(144)
plt.imshow(image_ori1)

    
        
#    def filter_image(img_org):
##        print(img_org.shape)
#        num_image = img_org.shape[0]
#        w_image = img_org.shape[1]
#        H_image = img_org.shape[2]
##        a = img_org[1,:,:,0].reshape([w_image,H_image])
##        print(a.shape)
#        for k in range(num_image):
#            
#            img =skimage.filters.gaussian(img_org[k,:,:,0].reshape([w_image,H_image]),sigma = 0.4)
##            print(img.shape)
#            img_arr = np.array(img)
#            img_binary = filters.threshold_otsu(img_arr)
#
#            for i in range(w_image):
#                for j in range(H_image):
#                    if(img_arr[i,j] <= img_binary):
#                        img_arr[i,j] = 0
#                    else:
#                        img_arr[i,j] = 1
#    #img_binary = img.convert("1")
#            dst2 = sm.erosion(img_arr,sm.square(5))
##            print(dst2.shape).reshape([w_image,H_image])
#            img_org[k,:,:,0] = dst2
#        return img_org 
#    def image_binary(img_org):
#        
#        num_image = img_org.shape[0]
#        w_image = img_org.shape[1]
#        H_image = img_org.shape[2]
#
#        for k in range(num_image):
#            
#            img =skimage.filters.gaussian(img_org[k,:,:,0].reshape([w_image,H_image]),sigma = 0.4)
#
#            img_arr = np.array(img)
#
#            dst2 = sm.erosion(img_arr,sm.square(5))
#
#            for i in range(w_image):
#                for j in range(H_image):
#                    if(img_arr[i,j] == 1.0):
#                        img_arr[i,j] = 1
#                    
#                    elif(img_arr[i,j] == -1.0):
#                        img_arr[i,j] = 1
#                    else:
#                        img_arr[i,j] = 0
#           
##            print(dst2.shape).reshape([w_image,H_image])
#            img_org[k,:,:,0] = dst2
#        return img_org