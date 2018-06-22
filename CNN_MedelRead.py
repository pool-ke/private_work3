#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 06:43:27 2018

@author: root
"""

import cv2
import skimage.io as io
import tensorflow as tf
import matplotlib.pyplot as plt
import math
import os
import numpy as np

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "3"
model_path = "./model_CNN"

img_size1=64
img_size2=32

n_classes=2
classes=['OK','NG']

#def compute_accuracy(v_xs,v_ys,keep_prob):
#    global prediction
#    y_pre=sess.run(prediction,feed_dict={Xs:v_xs,keep_prob:keep_prob})
#    correct_prediction=tf.equal(tf.argmax(y_pre,1),tf.arg_max(v_ys,1))
#    accuracy=tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
#    result=sess.run(accuracy,feed_fict={Xs:v_xs,ys:v_ys,keep_prob:keep_prob})
#    return result

def weight_variable(shape):
    initial=tf.truncated_normal(shape,stddev=0.1,dtype=tf.float32)
    return tf.Variable(initial)

def bias_variable(shape):
    initial=tf.constant(0.1,shape=shape,dtype=tf.float32)
    return tf.Variable(initial)

def conv_3d(x,W):
    return tf.nn.conv3d(x,W,strides=[1,1,1,1,1],padding='SAME')

def conv_2d(x,W):
    return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

def avg_pool_2x2(x):
    return tf.nn.avg_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

def max_pool_4x4(x):
    return tf.nn.max_pool(x,ksize=[1,4,4,1],strides=[1,4,4,1],padding='SAME')

def norm(x):
    return tf.nn.lrn(x,4,bias=10,alpha=0.001/9.0,beta=0.75)

tf.reset_default_graph()
Xs=tf.placeholder(tf.float32,[None,img_size1*img_size2])
ys=tf.placeholder(tf.float32,[None,n_classes])

X_img=tf.reshape(Xs,[-1,img_size1,img_size2,1])
keep_prob=tf.placeholder(tf.float32)
##conv1 layer
W_conv1=weight_variable([1,1,1,16])
b_conv1=bias_variable([16])
h_conv1=tf.nn.relu(conv_2d(X_img,W_conv1)+b_conv1)
h_pool1=max_pool_2x2(h_conv1)
h_norm1=norm(h_pool1)

##conv2 layer
W_conv2=weight_variable([5,5,16,32])
b_conv2=bias_variable([32])
h_conv2=tf.nn.relu(conv_2d(h_norm1,W_conv2)+b_conv2)
h_pool2=max_pool_2x2(h_conv2)
h_norm2=norm(h_pool2)

##conv3 layer
W_conv3=weight_variable([3,3,32,64])
b_conv3=bias_variable([64])
h_conv3=tf.nn.relu(conv_2d(h_norm2,W_conv3)+b_conv3)
h_pool3=max_pool_2x2(h_conv3)
h_norm3=norm(h_pool3)

##conv4 layer
W_conv4=weight_variable([3,3,64,128])
b_conv4=bias_variable([128])
h_conv4=tf.nn.relu(conv_2d(h_norm3,W_conv4)+b_conv4)
h_pool4=max_pool_2x2(h_conv4)
h_norm4=norm(h_pool4)

##func1 layer
W_func1=weight_variable([4*2*128,512])
b_func1=bias_variable([512])
h_norm4_flat=tf.reshape(h_norm4,[-1,4*2*128])
h_func1=tf.nn.relu(tf.matmul(h_norm4_flat,W_func1)+b_func1)
h_func1_drop=tf.nn.dropout(h_func1,keep_prob)

##func2 layer
W_func2=weight_variable([512,128])
b_func2=bias_variable([128])
h_func2=tf.nn.relu(tf.matmul(h_func1_drop,W_func2)+b_func2)
h_func2_drop=tf.nn.dropout(h_func2,keep_prob)

##func3 layer
W_func3=weight_variable([128,n_classes])
b_func3=bias_variable([n_classes])
prediction=tf.nn.softmax(tf.matmul(h_func2_drop,W_func3)+b_func3)
correct_prediction=tf.equal(tf.argmax(prediction,1),tf.argmax(ys,1))
Accuracy_tf=tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
cross_entropy=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction,labels=ys))

optimizer=tf.train.AdamOptimizer(0.0001)
train_step=optimizer.minimize(cross_entropy)

#train_step = tf.train.AdamOptimizer(0.0001).minimize(cross_entropy)

#sess=tf.Session()
#sess.run(tf.global_variables_initializer())

def test_model(image):
    img_flatted=image.flatten()
    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess = sess, coord = coord)
        saver.restore(sess,"./Model_CNN/model.ckpt")#./Model/model.ckpt
    
        pred=sess.run(prediction,{Xs:img_flatted,keep_prob:0.7})
        coord.request_stop()
        coord.join(threads)
        tmp=np.argmax(pred,axis=1)
        return tmp
