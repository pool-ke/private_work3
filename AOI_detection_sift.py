#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 01:36:30 2018

@author: root
"""
import os
import skimage
import numpy as np
import cv2
import copy

file_path_OK_pro='AOIDetection_pro/OK/'
file_path_NG_pro='AOIDetection_pro/NG/'
file_path_template='AOIDetection_pro/OK/SC0402-BGA_37.png'

if __name__=='__main__':
    AllFiles=os.listdir(file_path_OK_pro)
    for i in range(len(AllFiles)):
        file_path_test=file_path_OK_pro+AllFiles[i]
        img_test=cv2.imread(file_path_test)
        
