#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 15:20:11 2018

@author: root
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 10:39:05 2018

@author: root
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 12:03:25 2018

@author: root
"""
import numpy as np
import math
from PIL import Image,ImageFilter
#from scipy.ndimage import filters
import skimage.morphology as sm
import matplotlib.pyplot as plt
import tensorflow as tf
from skimage import filters,io, measure, color
import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "2"
#imread LOGO image from the current folder 


def read_and_decode(filename, W_img, H_img, flag):  #imread  Logo_train.tfrecords
    filename_queue = tf.train.string_input_producer([filename]) #produce a queue 
    
    reader = tf.TFRecordReader()
    _,serialized_example = reader.read(filename_queue)#return the file name and file
    features = tf.parse_single_example(serialized_example,
                                       features = {
                                               'label': tf.FixedLenFeature([], tf.int64),
                                               'img_raw': tf.FixedLenFeature([], tf.string),
                                               
                                               })#get the iamge data and label
    img =tf.decode_raw(features['img_raw'], tf.uint8)
    
    img = tf.reshape(img, [W_img,H_img,1]) # reshape an image to size
    #img = tf.cast(img, tf.float32) * (1./255) - 0.5 #give the tensor of image
    label = tf.cast(features['label'], tf.int32)
    if flag == 1:
    
        images, labels = tf.train.shuffle_batch([img, label],batch_size=5,
                                                capacity = 8000,
                                                num_threads = 1,
                                                min_after_dequeue = 2000)
    elif flag == 2:
        images, labels = tf.train.batch([img, label],batch_size = 20,
                                                capacity = 8000)
    elif flag == 3:
        images, labels = tf.train.shuffle_batch([img, label],batch_size = 20,
                                                capacity = 8000,
                                                num_threads = 1,
                                                min_after_dequeue = 2000)
    elif flag == 4:
         images, labels = tf.train.batch([img, label], batch_size = 20, 
                                        capacity = 8000)
            
    return  images, labels

#Black_Summar:92*1021
#black_Huawei:526*531
#Blue_Summar:81*793
#Blue_Huawei:427*435
#65*389
# 94*498
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
loss = tf.nn.l2_loss(targets_ - outputs_)
cost = tf.reduce_mean(loss, name = 'cost')
#
#optimal function
learning_rate = 0.001
optimizer = tf.train.AdamOptimizer(learning_rate).minimize(loss)


#noise_factor = 0.5
#img = mnist.test.images[10]
#noisy_img = img + noise_factor * np.random.randn(*img.shape)
#noisy_img = np.clip(noisy_img, 0.0,1.0)
#start
#sess = tf.Session()


def train_model(path_train):
#    W_img = 695
#    H_img = 161
    epochs = 10000
    img, label = read_and_decode(path_train, W_img, H_img,flag = 1)
    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess = sess, coord = coord)
        for i in range(epochs):
          
            val, _ = sess.run([img, label])
            
            val = val/255.0
    
            if i % 10 ==0:
                saver.save(sess,"model/CV_20180406_ROI1_1/model.ckpt")
                print("model saved")
            batch_cost, _ = sess.run([cost, optimizer], feed_dict = {inputs_: val,targets_: val})
            print("Epoch: {}/{}".format(i+1,epochs),
              "Training loss: {:.4f}".format(batch_cost))
        coord.request_stop()
        coord.join(threads)  
    ########## test -----get the code of an image in convolution 3
        
        #sess.run(tf.global_variables_initializer())
    #    coord2 = tf.train.Coordinator()
    #    threads2 = tf.train.start_queue_runners(sess = sess, coord = coord2)/home/huawei/myfile/code_python/Feng/Model1_Lan_HUAWEI/
    #  
def test_model(path_postive, path_negtive):
    img_postvie, label2_postive = read_and_decode(path_postive, W_img, H_img, flag = 2)
    img_negtive, label2_negtive = read_and_decode(path_negtive, W_img, H_img, flag = 2)#/home/huawei/myfile/code_python/Feng/tensorflow/LOGO_train_NG_695.tfrecords
    saver2 = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess = sess, coord = coord)
        
         ##postive samples
        val_re_postive, _ = sess.run([img_postvie, label2_postive])
        val_normal = val_re_postive/255.0
       
        #negtive samples
        val_re_negtive, _ = sess.run([img_negtive, label2_negtive])
        val2_normal= val_re_negtive/255.0
        
        #load the model5ckpu
#        saver2.restore(sess,"./model/MHA_HUAWEI_train1/model.ckpt")#./Model/model.ckpt
        saver2.restore(sess,"./model/MHA_model_train5/model.ckpt")
        
        #reconstruct the image by neurnetwork
        outp_postive = sess.run(outputs_, feed_dict = {inputs_: val_normal})
        outp_negtive = sess.run(outputs_, feed_dict = {inputs_: val2_normal})
        
        coord.request_stop()
        coord.join(threads)
#        print("Test is Over")
#        np.savetxt('img.txt',outp[1,:,:,0])
#        fig,axes = plt.subplots(nrows = 2, ncols = 5, sharex = True,figsize = (10,8))   
#        for image, row in zip([val2,outp], axes):
#            for img, ax in zip(image, row):
#               # print(image)
#                ax.imshow(img.reshape(695,161),cmap=plt.cm.gray)
#                ax.get_xaxis().set_visible(False)
#                ax.get_yaxis().set_visible(False)       
#        fig.tight_layout(pad=0.1)

        number_area_negtive = []#store the number of areas in an image 
        number_area_postive = []
        
        
        
        val22 = np.zeros(outp_negtive[:,:,:,0].shape)
        print(outp_negtive[:,:,:,0].shape)
        val22_ng = np.zeros(outp_negtive[:,:,:,0].shape)
        val12 = np.zeros(outp_negtive[:,:,:,0].shape)
        val13 = np.zeros(outp_negtive[:,:,:,0].shape)
        
        
        filter_weigth = 0.6
        
        for i in range(20):
            ###original images for postiveimg_ROI
            
#            num_for_open_before = 2
            img_pos_org_filter=filters.gaussian(val_normal[i,:,:,0], filter_weigth)
            thresh = filters.threshold_otsu(img_pos_org_filter)
            dst_pos_input = (img_pos_org_filter>=thresh)*1.0
            val22[i,:,:] = dst_pos_input
            ###reconstrruction images for postive
            img_pos_out_filter=filters.gaussian(outp_postive[i,:,:,0], filter_weigth)
            thresh = filters.threshold_otsu(img_pos_out_filter)
            dst2_pos_reconstruction = (img_pos_out_filter>=thresh)*1.0
            val22_ng[i,:,:] = dst2_pos_reconstruction
            
            
            ####orginal images for negtive
            img_neg_org_filter=filters.gaussian(val2_normal[i,:,:,0], filter_weigth)
            thresh = filters.threshold_otsu(img_neg_org_filter)
            dst_neg_input = (img_neg_org_filter>=thresh)*1.0
            
            ####reconstruction image for negtive
            img_neg_out_filter=filters.gaussian(outp_negtive[i,:,:,0], filter_weigth)
            thresh = filters.threshold_otsu(img_neg_out_filter)
            dst2_neg_reconstruction = (img_neg_out_filter>=thresh)*1.0

            val12[i,:,:] = dst2_neg_reconstruction

#            
#            org_img = sm.opening(dst,sm.square(5))
#            out_img = sm.opening(dst2,sm.square(5))rror (see above for traceba

            num_for_open = 4 #step for opening operator
            
#######postive image processing
            im_pos = np.abs(dst2_pos_reconstruction - dst_pos_input)
#            im_pos = sm.erosion(im_pos,sm.square(5))
#            im_pos = sm.dilation(im_pos,sm.square(5))
            im_pos = sm.opening(im_pos,sm.square(num_for_open))


#######negtive image processing 
            im_neg=np.abs(dst2_neg_reconstruction - dst_neg_input)
#            im_neg= sm.erosion(im_neg,sm.square(5))
#            im_neg=sm.dilation(im_neg,sm.square(5))
            im_neg = sm.opening(im_neg,sm.square(num_for_open))
            val13[i,:,:] = im_neg
            #dst=(dst<thresh)*0.0
            #dst=255-dst
#            print(im3.shape)
           
########positve area calculation
            labels_pos = measure.label(im_pos,connectivity = 2)
            num_area_pos = labels_pos.max()
            number_area_postive.append(num_area_pos)       
 
#######negtive area calculation           
            labels_neg = measure.label(im_neg,connectivity = 2)
            num_area_neg = labels_neg.max()
            number_area_negtive.append(num_area_neg)
#        np.savetxt('num_of_area.txt',number_area)
    ##calculate the precise and recall of the classification of anomalious images
        FN = 0
        TN = 0
        TP = 0
        FP = 0
        for x in number_area_postive:
            print(x)
            if x == 0:
                TN +=1
            elif x != 0:
                FP +=1
                
        
        for y in number_area_negtive:
            if y != 0:
                TP +=1
            elif y == 0:
                FN +=1        
                
        
        Precise = TP/ (TP + FP)
        Recall = TP / (TP + FN)
        
  
        
        
        print('Precise=:', Precise)
        print('Recall=:', Recall)
        print('TN=:', TN)
        print('FN=:', FN)
        print('TP=:', TP)
        print('FP=:', FP)
                
        
#    fig,axes = plt.subplots(nrows = 2, ncols = 5, sharex = True,figsize = (10,8))   
#    for image, row in zip([val12,val13], axes):
#        for img, ax in zip(image, row):
#           # print(image)
#            ax.imshow(img.reshape(W_img,H_img),cmap=plt.cm.gray)
#            ax.get_xaxis().set_visible(False)
#            ax.get_yaxis().set_visible(False)       
#    fig.tight_layout(pad=0.1)     
        

                
#        Recall_image = 
def test_model2(path_postive):
    img_postvie, label2_postive = read_and_decode(path_postive, W_img, H_img, flag = 2)#/home/huawei/myfile/code_python/Feng/tensorflow/LOGO_train_NG_695.tfrecords
    saver2 = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess = sess, coord = coord)
        
         ##postive samples
        val_re_postive, _ = sess.run([img_postvie, label2_postive])
        val_normal = val_re_postive/255.0
       
        
        #load the model5ckpu
#        saver2.restore(sess,"./model/MHA_HUAWEI_train1/model.ckpt")#./Model/model.ckpt
        saver2.restore(sess,"./model/CV_20180329_ROI_1_1/model.ckpt")
        
        #reconstruct the image by neurnetwork
        outp_postive = sess.run(outputs_, feed_dict = {inputs_: val_normal})
        
        coord.request_stop()
        coord.join(threads)
#        print("Test is Over")
#        np.savetxt('img.txt',outp[1,:,:,0])
#        fig,axes = plt.subplots(nrows = 2, ncols = 5, sharex = True,figsize = (10,8))   
#        for image, row in zip([val2,outp], axes):
#            for img, ax in zip(image, row):
#               # print(image)
#                ax.imshow(img.reshape(695,161),cmap=plt.cm.gray)
#                ax.get_xaxis().set_visible(False)
#                ax.get_yaxis().set_visible(False)       
#        fig.tight_layout(pad=0.1)

        number_area_negtive = []#store the number of areas in an image 
        number_area_postive = []
        
        
        
        val22 = np.zeros(outp_postive[:,:,:,0].shape)
        print(outp_postive[:,:,:,0].shape)
        val22_ng = np.zeros(outp_postive[:,:,:,0].shape)
        val12 = np.zeros(outp_postive[:,:,:,0].shape)
        val13 = np.zeros(outp_postive[:,:,:,0].shape)
        
        
        filter_weigth = 0.6
        
        for i in range(20):
            ###original images for postiveimg_ROI
            
#            num_for_open_before = 2
            img_pos_org_filter=filters.gaussian(val_normal[i,:,:,0], filter_weigth)
            thresh = filters.threshold_otsu(img_pos_org_filter)
            dst_pos_input = (img_pos_org_filter>=thresh)*1.0
            val22[i,:,:] = dst_pos_input
            ###reconstrruction images for postive
            img_pos_out_filter=filters.gaussian(outp_postive[i,:,:,0], filter_weigth)
            thresh = filters.threshold_otsu(img_pos_out_filter)
            dst2_pos_reconstruction = (img_pos_out_filter>=thresh)*1.0
            val22_ng[i,:,:] = dst2_pos_reconstruction
            
            
            ####orginal images for negtive

#            
#            org_img = sm.opening(dst,sm.square(5))
#            out_img = sm.opening(dst2,sm.square(5))rror (see above for traceba

            num_for_open = 4 #step for opening operator
            
#######postive image processing
            im_pos = np.abs(dst2_pos_reconstruction - dst_pos_input)
#            im_pos = sm.erosion(im_pos,sm.square(5))
#            im_pos = sm.dilation(im_pos,sm.square(5))
            im_pos = sm.opening(im_pos,sm.square(num_for_open))


#######negtive image processing
            #dst=(dst<thresh)*0.0
            #dst=255-dst
#            print(im3.shape)
           
########positve area calculation
            labels_pos = measure.label(im_pos,connectivity = 2)
            num_area_pos = labels_pos.max()
            number_area_postive.append(num_area_pos)       
 

#        np.savetxt('num_of_area.txt',number_area)
    ##calculate the precise and recall of the classification of anomalious images
        FN = 0
        TN = 0
        TP = 0
        FP = 0
        for x in number_area_postive:
            print(x)
            if x == 0:
                TN +=1
            elif x != 0:
                FP +=1
        
        print('TN=:', TN)
        print('FN=:', FN)
        print('TP=:', TP)
        print('FP=:', FP)
def main():
    path_train = '/home/huawei/CV_20180426_data/Logo_ROI1_1.tfrecords'#"/home/huawei/myfile/code_python/Feng/dataset_tfrecord/Lan_HUAWEI/LOGO_train_Lan_HUAWEI_OK.tfrecords"
#    path_postive = '/home/huawei/CV_20180329_data/20180329ROI1/Logo_ROI1_1_test2.tfrecords'
#    path_negtive = '/home/huawei/Kyaoshi/MHA_Hui_0926_ROI/Model/Logo_NG_full.tfrecords'

#    path_train = "/home/huawei/myfile/code_python/Feng/dataset_tfrecord/LOGO_train_New_ok.tfrecords"
#    path_postive = "/home/huawei/myfile/code_python/Feng/dataset_tfrecord/LOGO_train_New_ok.tfrecords"
#    path_negtive = "/home/huawei/myfile/code_python/Feng/dataset_tfrecord/LOGO_train_New_ng.tfrecords"
#    path_negtive = "/home/huawei/myfile/code_python/Feng/dataset_tfrecord/Lan_HUAWEI/LOGO_train_Lan_HUAWEI_OK.tfrecords"
#    
    train_model(path_train)
###    conv_autoencoder.train(batch_size=100, passes=20000, new_training=True)
#    test_model(path_postive, path_negtive)
#    test_model2(path_postive)


if __name__ == '__main__':
    main()
   
    
    
