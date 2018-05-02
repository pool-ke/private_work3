#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 09:50:52 2018

@author: root
"""

import os
import numpy as np
import cv2 as cv 
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import KFold

Ori_file_path="/home/huawei/Kyaoshi/v_ZuanLan_0926_ROI_20/HUAWEI/OK/"


file_list=os.listdir(Ori_file_path)

print (file_list)

#file_path = Ori_file_path+"/"+file_list[99]
#img1=cv.imread(file_path)
#print (img1)
#file_path2="/home/huawei/Kyaoshi/v_ZuanLan_0926_ROI/SUM/"+file_list[99]
#cv.imwrite(file_path2,img1)

num=range(len(file_list))
num=list(num)
#print (num)
y=np.zeros(len(file_list))
#y=list(y)
#ss=StratifiedShuffleSplit(n_splits=5,test_size=0.1,train_size=0.9,random_state=None)
#folder=KFold(n_splits=5,random_state=0,shuffle=False)
sfolder=StratifiedKFold(n_splits=5,random_state=4,shuffle=True)

#for train_index,test_index in ss.split(num,y):
#    print (len(train_index))
#    print (len(test_index))
    
#    print (" ")
#    for j in test_index:
#        print (j,end='')
#    print (" ")
#print (len(file_list))
#print (file_list)

#print ("""""""""""""""""")
#for train_index,test_index in folder.split(num,y):
#    print (train_index)
#    print (test_index)
#print ("""""""""""""""""")
i=1    
for train_index,test_index in sfolder.split(num,y):
    train_file_path="/home/huawei/Kyaoshi/v_ZuanLan_0926_ROI_20/HUAWEI/train"+str(i)+"/"
    test_file_path="/home/huawei/Kyaoshi/v_ZuanLan_0926_ROI_20/HUAWEI/test"+str(i)+"/"
    for index_train in train_index:
        file_path_read=Ori_file_path+file_list[index_train]
        img1=cv.imread(file_path_read)
        print (file_path_read)
        file_path_write=train_file_path+file_list[index_train]
        cv.imwrite(file_path_write,img1)
        print (file_path_write)
    for index_test in test_index:
        file_path_read=Ori_file_path+file_list[index_test]
        img2=cv.imread(file_path_read)
        print (file_path_read)
        file_path_write=test_file_path+file_list[index_test]
        cv.imwrite(file_path_write,img2)
        print (file_path_write)
    print (i)
    i+=1
    