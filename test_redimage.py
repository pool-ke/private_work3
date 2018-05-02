#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 16:01:21 2017

@author: root
"""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
import tensorflow as tf

cwd = '/home/huawei/CV_20180426_data/'
classes = {'train'}#two classifies

writer = tf.python_io.TFRecordWriter("/home/huawei/CV_20180426_data/Logo_ROI1_1.tfrecords")#the file need to be produced

for index, name in enumerate(classes):
    class_path = cwd + name + '/'
    for img_name in os.listdir(class_path):
        img_path = class_path + img_name #the direction of each image
        #print(img_path)
        img = Image.open(img_path).convert("L")
        img = img.resize((161,353))
        img_raw = img.tobytes()#transform image to byte
        example = tf.train.Example(features = tf.train.Features(feature={
                "label": tf.train.Feature(int64_list = tf.train.Int64List(value = [index])),
                "img_raw": tf.train.Feature(bytes_list = tf.train.BytesList(value = [img_raw]))}))
        #print(example)
        writer.write(example.SerializeToString()) #xulie transform to zifu
        #print(writer)
writer.close()
    
def read_and_decode(filename):  #imread  Logo_train.tfrecords
    filename_queue = tf.train.string_input_producer([filename]) #produce a queue 
    
    reader = tf.TFRecordReader()
    _,serialized_example = reader.read(filename_queue)#return the file name and file
    features = tf.parse_single_example(serialized_example,
                                       features = {
                                               'label': tf.FixedLenFeature([], tf.int64),
                                               'img_raw': tf.FixedLenFeature([], tf.string),
                                               })#get the iamge data and label
    img =tf.decode_raw(features['img_raw'], tf.uint8)
    img = tf.reshape(img, [353,161,1]) # reshape an image to size
    #img = tf.cast(img, tf.float32) * (1./255) - 0.5 #give the tensor of image
    label = tf.cast(features['label'], tf.int32)
    images, labels = tf.train.shuffle_batch([img, label],batch_size = 4,
                                            capacity = 8000,
                                            num_threads = 4,
                                            min_after_dequeue = 2000)
    return  images, labels

#
#filename_queue = tf.train.string_input_producer(["LOGO_train.tfrecords"])
#reader = tf.TFRecordReader()
#_, serialized_example = reader.read(filename_queue)#return the file name and file
#features = tf.parse_single_example(serialized_example,
#                                   features = {
#                                           'label': tf.FixedLenFeature([], tf.int64),
#                                           'img_raw': tf.FixedLenFeature([], tf.string),
#                                           })#get the iamge data and label
#image =tf.decode_raw(features['img_raw'], tf.uint8)
#image = tf.reshape(image, [128,128,1]) # reshape an image to size
#label = tf.cast(features['label'], tf.int32)
#
#with tf.Session() as sess:
#    init_op = tf.initialize_all_variables()
#    sess.run(init_op)
#    coord = tf.train.Coordinator()
#    threads = tf.train.start_queue_runners(coord = coord)
#    for i in range(20):
#        example, l = sess.run([image, label])# get the images and labels
#        
#        img = example.reshape([128,128])
#        img = Image.fromarray(img)
#        img.save(cwd + str(i) + '_''Label_' + str(l) + '.bmp')#save the image
#        print(example.shape, l)
#    coord.request_stop()
#    coord.join(threads)
#
#img, label = read_and_decode("/home/huawei/CV_20180329_data/20180329ROI1/Logo_ROI1_1_train.tfrecords")

img, label = read_and_decode("/home/huawei/CV_20180426_data/Logo_ROI1_1.tfrecords")
#use shuffle_bath random arrange the images

img_batch, label_batch = tf.train.shuffle_batch([img, label], batch_size = 10, capacity = 40, min_after_dequeue = 20)


init = tf.initialize_all_variables()

with tf.Session() as sess:
    sess.run(init)
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord = coord)
    for i in range(1):
        val, l = sess.run([img, label])

        #print(val.shape, l)  
        fig,axes = plt.subplots(nrows = 1, ncols = 4, sharex = True,figsize = (10,8))
        for img, ax in zip(val, axes):
            ax.imshow(img.reshape(353,161),cmap=plt.cm.gray)
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)       
        fig.tight_layout(pad=0.1)
#            