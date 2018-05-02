#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 14:34:56 2018

@author: root
"""

import numpy as np
from PIL import Image
import skimage.morphology as sm
import matplotlib.pyplot as plt
import tensorflow as tf
from skimage import filters,io, measure, color
import os
import math
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "2"

W_img = 353
H_img = 161

inputs_ = tf.placeholder(tf.float32,(None, W_img, H_img, 1), name = 'inputs_')
targets_ = tf.placeholder(tf.float32,(None, W_img, H_img, 1), name = 'targets_')
#hidden layer

conv1_d = tf.layers.conv2d(inputs_,32, (3,3), padding = 'same', activation = tf.nn.relu, name = 'conv1_d')
conv1_p = tf.layers.max_pooling2d(conv1_d, (2,2),(2,2), padding = 'same', name = 'conv1_p')

conv2_d = tf.layers.conv2d(conv1_p,32, (3,3), padding = 'same', activation = tf.nn.relu, name = 'conv2_d')
conv2_p = tf.layers.max_pooling2d(conv2_d, (2,2),(2,2), padding = 'same', name = 'conv2_p')

conv3_d = tf.layers.conv2d(conv2_p,32, (3,3), padding = 'same', activation = tf.nn.relu, name = 'conv3_d')
conv3_p = tf.layers.max_pooling2d(conv3_d, (2,2),(2,2), padding = 'same', name = 'conv3_p')

conv_3_d = tf.layers.conv2d(conv3_p,32, (3,3), padding = 'same', activation = tf.nn.relu, name = 'conv_3_d')
conv_3_p = tf.layers.max_pooling2d(conv_3_d, (2,2),(2,2), padding = 'same', name = 'conv_3_p')

full_W = math.ceil(W_img/16.0)
full_H = math.ceil(H_img/16.0)

in_full_connect = tf.reshape(conv_3_p,[-1,full_W*full_H*32], name = 'in_full_connect')#upfold the tensor
full_connect = tf.layers.dense(in_full_connect, 50, activation = tf.nn.relu, name = 'full_connect')# connect with full

#decoder layer
de_full_connect = tf.layers.dense(full_connect, full_W*full_H*32, activation = tf.nn.relu, name = 'de_full_connect')#connect with full
de_full = tf.reshape(de_full_connect,[-1,full_W,full_H,32], name = 'de_full')# huifu to the same shape of tensor

conv_4_n = tf.image.resize_nearest_neighbor(de_full,(2*full_W,2*full_H), name = 'conv_4_n')
conv_4_d = tf.layers.conv2d(conv_4_n, 32, (3,3),padding = 'same',activation = tf.nn.relu, name = 'conv_4_d')

conv4_n = tf.image.resize_nearest_neighbor(conv_4_d,(4*full_W,4*full_H), name = 'conv4_n')
conv4_d = tf.layers.conv2d(conv4_n, 32, (3,3),padding = 'same',activation = tf.nn.relu, name = 'conv4_d')

conv5_n = tf.image.resize_nearest_neighbor(conv4_d,(8*full_W,8*full_H), name = 'conv5_n')
conv5_d = tf.layers.conv2d(conv5_n, 32, (3,3),padding = 'same',activation = tf.nn.relu, name = 'conv5_d')

conv6_n = tf.image.resize_nearest_neighbor(conv5_d,(W_img, H_img), name = 'conv6_n')
conv6_d = tf.layers.conv2d(conv6_n,32, (3,3),padding = 'same',activation = tf.nn.relu, name = 'conv6_d')

logits_ = tf.layers.conv2d(conv6_d, 1, (3,3), padding = 'same', activation = None, name = 'logits_')
outputs_ = tf.nn.sigmoid(logits_, name = 'outputs_')

#loss function
#loss = tf.nn.sigmoid_cross_entropy_with_logits(labels = targets_, logits = logits_, name = 'loss')
#cost = tf.reduce_mean(loss, name = 'cost')

#loss function
loss = tf.nn.l2_loss(targets_ - outputs_)
cost = tf.reduce_mean(loss, name = 'cost')
#
#optimal function
learning_rate = 0.001
optimizer = tf.train.AdamOptimizer(learning_rate).minimize(loss)

def test_model(image_input):
#    img2, label2 = read_and_decode("/home/huawei/myfile/code_python/Feng/LOGO_train_More_15.tfrecords",flag = 4)#/home/huawei/myfile/code_python/Feng/tensorflow/LOGO_train_NG_695.tfrecords
    saver2 = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess = sess, coord = coord)
#        val2, _ = sess.run([img2, label2])
#        val2 = val2/255.0
        saver2.restore(sess,"./model/CV_20180406_ROI1_1/model.ckpt")#./Model/model.ckpt
#        saver2.restore(sess,"./model/CV_20180329_ROI_1_1/model.ckpt")#
        outp = sess.run(outputs_, feed_dict = {inputs_: image_input})
        coord.request_stop()
        coord.join(threads)
        return outp