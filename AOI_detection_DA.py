#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 02:30:38 2018

@author: root
"""

import cv2
import os
import numpy as np
import copy

file_path_OK_pro='AOIDetection_pro/OK/'
file_path_NG_pro='AOIDetection_pro/NG/'

file_path_OK_DA='AOIDetection_da/OK/'
file_path_NG_DA='AOIDetection_da/NG/'

if __name__=='__main__':
#    #positive samples preprocess
#    AllFiles=os.listdir(file_path_OK_pro)
#    for i in range(len(AllFiles)):
#        file_path_read=file_path_OK_pro+AllFiles[i]
#        img_test=cv2.imread(file_path_read)
#        for j in range(4):
#            for k in range(5):
#                print (j)
#                print (k)
#                file_path_save=file_path_OK_DA+str(j)+'_'+str(k)+'_'+AllFiles[i]
#                img_pro=copy.copy(img_test[2*j:2*j+64,3*k:3*k+32])
#                cv2.imwrite(file_path_save,img_pro)
    #negative samples preprocess
    AllFiles=os.listdir(file_path_NG_pro)
    for i in range(len(AllFiles)):
        file_path_read=file_path_NG_pro+AllFiles[i]
        img_test=cv2.imread(file_path_read)
        for j in range(4):
            for k in range(5):
                print (j)
                print (k)
                file_path_save=file_path_NG_DA+str(j)+'_'+str(k)+'_'+AllFiles[i]
                img_pro=copy.copy(img_test[2*j:2*j+64,3*k:3*k+32])
                cv2.imwrite(file_path_save,img_pro)
        