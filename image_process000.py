#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 14:35:33 2017

@author: root
"""

import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

file_path="photo002.png"
def addredlabel(im):
    cv.rectangle(im,(0,2),(161,695),(255,0,0),3)
def addbluelabel(im):
    im1=cv.rectangle(im,(0,2),(161,695),(0,0,255),3)
    return im1
im=cv.imread(file_path)
print (im)
im1=addbluelabel(im)
print (im)
#im1=cv.rectangle(im,(0,0),(161,695),(255,0,0),5)
#font=cv.InitFont(cv.CV_FONT_HERSHEY_SCRIPT_SIMPLEX,1,1,0,1,8)
#cv.putText(im,"OK",(30,0),font,(0,0,255))
#plt.figure()
#plt.imshow(im)