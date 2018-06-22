#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 31 01:06:41 2018

@author: root
"""

import os
import skimage
import numpy as np
import cv2

file_path_OK_ori='AOIDetection/OK/'
file_path_NG_ori='AOIDetection/NG/'
file_path_OK_pro='AOIDetection_pro/OK/'
file_path_NG_pro='AOIDetection_pro/NG/'

if(not os.path.exists(file_path_OK_pro)):
    print ("not exist!")
    os.mkdir(file_path_OK_pro)
if(not os.path.exists(file_path_NG_pro)):
    print ("not exist!")
    os.mkdir(file_path_NG_pro)

if __name__=='__main__':
    AllFiles=os.listdir(file_path_NG_ori)
    print (AllFiles)
    for i in range(len(AllFiles)):
        file_path_read=file_path_NG_ori+AllFiles[i]
        file_path_save=file_path_NG_pro+AllFiles[i]
        img_ori=cv2.imread(file_path_read)
        H=img_ori.shape[0]
        W=img_ori.shape[1]
        if (H==70):
            img_res=img_ori
        elif(H==45):
            img_res=np.rot90(img_ori)
        cv2.imwrite(file_path_save,img_res)
        
        
    
#    file_path_read=file_path_OK_ori+AllFiles[0]    
#    img_ori=cv2.imread(file_path_read)
#    print (img_ori.shape[0])
#    print (img_ori.shape[1])
#    img_rot=np.rot90(img_ori)
#    print (img_rot.shape[0])
#    print (img_rot.shape[1])
#    cv2.imshow("img_ori",img_ori)
#    cv2.imshow("img_rot",img_rot)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()