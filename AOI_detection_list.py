#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 31 03:59:07 2018

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

methods=['cv2.TM_CCOEFF','cv2.TM_CCOEFF_NORMED','cv2.TM_CCORR','cv2.TM_CCORR_NORMED','cv2.TM_SQDIFF','cv2.TM_SQDIFF_NORMED']
meth=methods[5]
method=eval(meth)

target_OK=[]
target_NG=[]

if __name__=='__main__':
    img_ori=cv2.imread(file_path_template)
    img_template=copy.copy(img_ori[8:45,20:38])
    ROI_H=37
    ROI_W=18
    
    AllFiles1=os.listdir(file_path_OK_pro)
    for i in range(len(AllFiles1)):
        print (AllFiles1[i])
        file_path_read=file_path_OK_pro+AllFiles1[i]
        img_test=cv2.imread(file_path_read)
        res=cv2.matchTemplate(img_test,img_template,method)
        min_val,max_val,min_loc,max_loc=cv2.minMaxLoc(res)
        if method in [cv2.TM_SQDIFF,cv2.TM_SQDIFF_NORMED]:
            top_left=min_loc
            target_val=min_val
        else:
            top_left=max_loc
            target_val=max_val
        target_OK.append(target_val)
        
    AllFiles2=os.listdir(file_path_NG_pro)
    for i in range(len(AllFiles2)):
        print (AllFiles2[i])
        file_path_read=file_path_OK_pro+AllFiles1[i]
        img_test=cv2.imread(file_path_read)
        res=cv2.matchTemplate(img_test,img_template,method)
        min_val,max_val,min_loc,max_loc=cv2.minMaxLoc(res)
        if method in [cv2.TM_SQDIFF,cv2.TM_SQDIFF_NORMED]:
            top_left=min_loc
            target_val=min_val
        else:
            top_left=max_loc
            target_val=max_val
        target_NG.append(target_val)
    print (target_OK)
    print (target_NG)