#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 14:20:21 2018

@author: root
"""

import sys
import cv2 as cv
import numpy as np
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog,QMessageBox,QSlider
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import skimage.morphology as sm
from skimage import filters
import skimage
import os
import copy
import CAE_modelread1 as df
#import CAEmodelread as df1

imgPath="/home/huawei/myfile/code_python/KE/ROI_Logo/H/OK/"
ptRslt=[]

class Figure_Canvas(FigureCanvas):
    def __init__(self,parent=None,width=4,height=3,dpi=100):
        fig=Figure(figsize=(width,height),dpi=100)
        FigureCanvas.__init__(self,fig)
        self.setParent(parent)
        
        self.axes=fig.add_subplot(111)
        
        
#    def test(self,w=1,X_line1=0,X_line2=100):
#        X=np.linspace(0,100,101,endpoint=True)
#        Y=wX
#        self.axes.plot(X,Y)
#        self.axes.vlines(X_line1,0,100,colors='c',linestyles="dashed")
#        self.axes.vlines(X_line2,0,100,colors='red',linestyles="dashed")
    def test(self,X_line1=0):
        X=np.linspace(0,100,101,endpoint=True)
        Y=np.zeros(len(X))
        for i in range(len(X)):
            Y[i]=int(X[i]/10)+1
        self.axes.plot(X,Y)
        self.axes.vlines(X_line1,0,11,colors='red',linestyles="dashed")


class Image_Process(QtWidgets.QWidget):
    def __init__(self):
        super(Image_Process,self).__init__()
        self.setGeometry(100,100,1300,900)
        self.setWindowTitle("Image_Process")
        self.initUI()
        self.imgOri=None
        self.imgOriIndex=None
        self.model=None
        self.modelIndex=None
        self.img_contrast=None
        self.img_contrastIndex=None
        self.img_processed=None
        self.position1=0
        self.position2=100
        self.index=1
    def initUI(self):
        self.label1=QtWidgets.QLabel(u'File_Path:',self)
        self.label1.move(10,20)
        self.editR=QtWidgets.QLineEdit(self)
        self.editR.move(70,18)
        self.editR.resize(300,18)
        
        self.buttonChoose=QtWidgets.QPushButton(u"ChooseFile",self)
        self.buttonChoose.move(375,18)
        self.buttonChoose.clicked.connect(self.choosefile)
        
        self.buttonLoad=QtWidgets.QPushButton(u"LoadFile",self)
        self.buttonLoad.move(470,18)
        self.buttonLoad.clicked.connect(self.loadfile)

        self.buttonProcess=QtWidgets.QPushButton(u"loadmodel",self)
        self.buttonProcess.move(565,18)
        self.buttonProcess.clicked.connect(self.img_process)
        
        self.buttonVisualize=QtWidgets.QPushButton(u"visualize",self)
        self.buttonVisualize.move(660,18)
        self.buttonVisualize.clicked.connect(self.img_visualize)
        
        self.buttonProcess2=QtWidgets.QPushButton(u"Process",self)
        self.buttonProcess2.move(755,18)
        self.buttonProcess2.clicked.connect(self.img_process2)
        
        self.buttonProcess3=QtWidgets.QPushButton(u"On/Off",self)
        self.buttonProcess3.move(850,18)
        self.buttonProcess3.clicked.connect(self.img_process3)
        
        self.buttonProcess4=QtWidgets.QPushButton(u"listprocess",self)
        self.buttonProcess4.move(945,18)
        self.buttonProcess4.clicked.connect(self.img_process4)
        
        self.labelload=QtWidgets.QLabel(self)
        self.labelload.move(1040,18)
        self.labelload.resize(100,20)
        
        
        self.allFiles=QtWidgets.QListWidget(self)
        self.allFiles.move(30,40)
        self.allFiles.resize(120,300)
        
        self.piclist=QtWidgets.QListWidget(self)
        self.piclist.move(30,350)
        self.piclist.resize(105,430)
        self.piclist.setIconSize(QtCore.QSize(80,398))
        self.piclist.setResizeMode(QtWidgets.QListView.Adjust)
        self.piclist.setViewMode(QtWidgets.QListView.IconMode)
        self.piclist.setMovement(QtWidgets.QListView.Static)
        self.piclist.setSpacing(10)
        

        
        self.label3=QtWidgets.QLabel(u'X1:',self)
        self.label3.move(1010,70)
        self.editX=QtWidgets.QLineEdit(self)
        self.editX.move(1030,70)
        self.editX.resize(50,18)
        
        self.label4=QtWidgets.QLabel(u'Y1:',self)
        self.label4.move(1010,100)
        self.editY=QtWidgets.QLineEdit(self)
        self.editY.move(1030,100)
        self.editY.resize(50,18)
        
        self.label5=QtWidgets.QLabel(u'thread1:',self)
        self.label5.move(1100,70)
        self.editX1=QtWidgets.QLineEdit(self)
        self.editX1.move(1150,70)
        self.editX1.resize(50,18)
        self.editX1.setText("3")
        
        self.label7=QtWidgets.QLabel(u'thread2:',self)
        self.label7.move(1100,130)
        self.editX2=QtWidgets.QLineEdit(self)
        self.editX2.move(1150,130)
        self.editX2.resize(50,18)
        self.editX2.setText("0")
        
        self.label6=QtWidgets.QLabel(u'Y2:',self)
        self.label6.move(1100,100)
        self.editY1=QtWidgets.QLineEdit(self)
        self.editY1.move(1150,100)
        self.editY1.resize(50,18)
#        allImgs=os.listdir(imgPath)
#        for imgTemp in allImgs:
#            self.allFiles.addItem(imgTemp)
#        print (self.allFiles.count())
        self.allFiles.itemClicked.connect(self.itemClick)
        self.piclist.itemClicked.connect(self.itemClick1)
        
#        self.label2=QtWidgets.QLabel(self)
#        self.label2.move(30,750)
#        self.label2.setText('Total Files:%d'%(int(self.allFiles.count())))
        self.labelImg1=QtWidgets.QLabel("Input_Image",self)
        self.labelImg1.move(200,70)
        self.labelImg1.resize(161,353)
        
        self.labelImg2=QtWidgets.QLabel("Output_Image",self)
        self.labelImg2.move(400,70)
        self.labelImg2.resize(161,353)
        
        self.labelImg3=QtWidgets.QLabel("Contrast_Image",self)
        self.labelImg3.move(600,70)
        self.labelImg3.resize(161,353)
        
        self.table=QtWidgets.QTableWidget(self)
        self.table.move(800,200)
        self.table.resize(400,80)
        self.table.setColumnCount(2)
        self.table.setRowCount(2)
        self.table.setHorizontalHeaderLabels(["Positive(predicted)","Negative(predicted)"])
        self.table.setVerticalHeaderLabels(["Positive(True)","Negative(True)"])
        self.table.setColumnWidth(0,145)
        self.table.setColumnWidth(1,145)
        
        self.label7=QtWidgets.QLabel("the Precision is %.2f %%"%(98.6852),self)
        self.label7.move(800,280)
        self.label7.resize(200,25)
        
        self.label8=QtWidgets.QLabel("the Recall is %.2f %%"%(98.6852),self)
        self.label8.move(800,305)
        self.label8.resize(200,25)
        
        self.label9=QtWidgets.QLabel("the F1 is %.2f %%"%(98.6852),self)
        self.label9.move(800,330)
        self.label9.resize(200,25)
        
        
        self.graphicview=QtWidgets.QGraphicsView(self)
        self.graphicview.move(800,350)
        self.graphicview.resize(400,450)
        
        self.sld1=QSlider(Qt.Horizontal,self)
        self.sld1.setFocusPolicy(Qt.NoFocus)
        self.sld1.move(850,750)
        self.sld1.resize(315,50)
        self.sld1.valueChanged[int].connect(self.sldvaluechange)
        
#        self.sld2=QSlider(Qt.Horizontal,self)
#        self.sld2.setFocusPolicy(Qt.NoFocus)
#        self.sld2.setValue(100)
#        self.sld2.move(850,550)
#        self.sld2.resize(315,50)
#        self.sld2.valueChanged[int].connect(self.sldvaluechange2)

    def binary_img(self,img_org,thread):
        H_image=img_org.shape[0]
        W_image=img_org.shape[1]
        img_binary = filters.threshold_otsu(img_org)
        print (img_binary)
        for i in range(H_image):
            for j in range(W_image):
                if(img_org[i,j] <= img_binary+thread):
                    img_org[i,j] = 0
                else:
                    img_org[i,j] = 255
#        img_org = sm.erosion(img_org,sm.square(3))
        return img_org
    def choosefile(self):
        directory1=QFileDialog.getExistingDirectory(self,"get directory","/home/huawei")
        self.editR.setText(str(directory1))
        
    def loadfile(self):
        imgPath=self.editR.text()
        print (imgPath)
        if os.path.isdir(imgPath):
            allImgs=os.listdir(imgPath)
            for imgTemp in allImgs:
                self.allFiles.addItem(imgTemp)
#            self.label2.setText('Total Files:%d'%(int(self.allFiles.count())))
                
        else:
            QMessageBox.information(self,"Warning","The Diretory is Not Exist!",QMessageBox.Ok)
            
        allImgs=os.listdir(imgPath)
        image_input=np.zeros((len(allImgs),353,161,1))
        for i in range(len(allImgs)):
            temp=imgPath+"/"+allImgs[i]
            print (temp)
            img1=cv.imread(temp)
            img_gray=cv.cvtColor(img1,cv.COLOR_BGR2GRAY)*(1./255)
            img_gray_temp=np.reshape(img_gray,(img_gray.shape[0],img_gray.shape[1],1))
            image_input[i]=img_gray_temp
        
        
        image_output=np.zeros((len(allImgs),353,161,1))
        sum_count=len(allImgs)
        count=len(allImgs)
        i=0
        batch_size=30
        while (count>0):
            if (count>=30):
                print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print (image_input[batch_size*i:batch_size*i+batch_size].shape)
                image_output_temp=df.test_model(image_input[batch_size*i:batch_size*i+batch_size])
                print (image_output_temp.shape)
                image_output[batch_size*i:batch_size*i+batch_size]=image_output_temp
                count=count-batch_size
                i=i+1
            else:
                image_output_temp=df.test_model(image_input[sum_count-count:sum_count])
                print (image_output_temp.shape)
                image_output[sum_count-count:sum_count]=image_output_temp
                count=0
        print (self.allFiles.count())
                
#        print (image_input.shape)
#        image_output=df.test_model(image_input)
#                
        
#        image_input_temp=image_input[0:20]
#        print (image_input_temp.shape)
#        image_output=df.test_model(image_input_temp)
#        print (image_output.shape)
#        image_output=np.zeros((len(allImgs),323,138,1))
#        for i in range(len(allImgs)):
#            image_output[i]=df.test_model(image_input[i])
#                
        allImgs=os.listdir(imgPath)
        for i in range(len(allImgs)):
            file_path="QTGUIMODEL/"+allImgs[i]
            image_temp=image_output[i]*255
            cv.imwrite(file_path,image_temp)
#        print (image_input[0:20].shape)
#        image_input_temp=image_input[20:40]        
#        image_output=df.test_model(image_input_temp)
#        print (image_output.shape)
        
        
    def itemClick(self):
        temp=self.editR.text()+"/"+self.allFiles.currentItem().text()
        temp1="QTGUIMODEL/"+self.allFiles.currentItem().text()
#        temp=imgPath+self.allFiles.currentItem().text()
        self.imgOri=cv.imread(str(temp))
        self.model=cv.imread(temp1)
        print (self.imgOri)
        height=self.imgOri.shape[0]
        ratioY=self.labelImg1.height()/(height+0.0)
        width=self.imgOri.shape[1]
        height2=self.labelImg1.height()
        width2=int(width*ratioY+0.5)
        img2=cv.resize(self.imgOri,(width2,height2))
        cv.imwrite("QTGUI/process001.png",img2)
        qImgT=QtGui.QPixmap("QTGUI/process001.png")
        qImgT1=QtGui.QPixmap(temp1)
        self.labelImg1.setPixmap(qImgT)
        self.labelImg2.setPixmap(qImgT1)
        self.index=1
    def itemClick1(self):
        temp=self.piclist.currentItem().text()
        print (temp)
        self.img_processed=cv.imread(temp)
        height=self.img_processed.shape[0]
        ratioY=self.labelImg1.height()/(height+0.0)
        width=self.img_processed.shape[1]
        height2=self.labelImg1.height()
        width2=int(width*ratioY+0.5)
        img2=cv.resize(self.img_processed,(width2,height2))
        cv.imwrite("QTGUI/process004.png",img2)
        qImgT=QtGui.QPixmap("QTGUI/process004.png")
        self.labelImg1.setPixmap(qImgT)
        
    
    def img_process(self):
        temp="photo002.png"
        self.model=cv.imread(temp)
        height=self.model.shape[0]
        ratioY=self.labelImg2.height()/(height+0.0)
        
        width=self.model.shape[1]
        height2=self.labelImg2.height()
        width=int(width*ratioY+0.5)
        img2=cv.resize(self.model,(width,height2))
        cv.imwrite("QTGUI/process002.png",img2)
        
        qImgT=QtGui.QPixmap("QTGUI/process002.png")
        self.labelImg2.setPixmap(qImgT)
#        img1=self.imgOri
#        img2=cv.GaussianBlur(img1,(5,5),1)
#        img3=cv.Canny(img2,90,100)
#        height=img3.shape[0]
#        ratioY=self.labelImg2.height()/(height+0.0)
#        
#        width=img3.shape[1]
#        height2=self.labelImg2.height()
#        width2=int(width*ratioY+0.5)
#        img4=cv.resize(img3,(width2,height2))
#        cv.imwrite("QTGUI/process002.png",img4)
#        
#        qImgT=QtGui.QPixmap("QTGUI/process002.png")
#        self.labelImg2.setPixmap(qImgT)
    def img_process2(self):
        img_temp1=copy.copy(self.imgOri[:,:,0])
        img_temp2=copy.copy(self.model[:,:,0])
        img1=self.binary_img(img_org=img_temp1)
        img2=self.binary_img(img_org=img_temp2)
        self.img_contrast=np.abs(img1-img2)
        img3=sm.opening(self.img_contrast,sm.square(3))
        height=img3.shape[0]
        ratioY=self.labelImg3.height()/(height+0.0)
        width=img3.shape[1]
        height2=self.labelImg3.height()
        width=int(width*ratioY+0.5)
        img2=cv.resize(img3,(width,height2))
        cv.imwrite("QTGUI/process003.png",img2)        
        qImgT=QtGui.QPixmap("QTGUI/process003.png")
        self.labelImg3.setPixmap(qImgT)
        
        self.img_processed=copy.copy(self.imgOri)
        height1=self.img_processed.shape[0]
        width1=self.img_processed.shape[1]
        
        count=0
        for i in range(height1):
            for j in range(width1):
                if img3[i][j]!=0:
                    self.img_processed[i][j][0]=255
                    self.img_processed[i][j][1]=0
                    self.img_processed[i][j][2]=0
                    count+=1
        print (count)            
        height=self.img_processed.shape[0]
        ratioY=self.labelImg1.height()/(height+0.0)
        width=self.img_processed.shape[1]
        height2=self.labelImg1.height()
        width=int(width*ratioY+0.5)
        img2=cv.resize(self.img_processed,(width,height2))
        cv.imwrite("QTGUI/process004.png",img2)        
        qImgT1=QtGui.QPixmap("QTGUI/process004.png")
        self.labelImg1.setPixmap(qImgT1)
        self.index=2
        
    def img_process3(self):
        if self.index==1:
            qImgT=QtGui.QPixmap("QTGUI/process004.png")
            self.labelImg1.setPixmap(qImgT)
            self.index=2
        else:
            qImgT=QtGui.QPixmap("QTGUI/process001.png")
            self.labelImg1.setPixmap(qImgT)
            self.index=1
            
    def img_process4(self):
        print (self.allFiles.count())
        self.labelload.setText("load begining!")
        thread1=self.editX1.text()
        value_thread1=int(thread1)
        thread2=self.editX2.text()
        value_thread2=int(thread2)
        print (value_thread1)
        for i in range(self.allFiles.count()):
            temp=self.editR.text()+"/"+self.allFiles.item(i).text()
            temp1="QTGUIMODEL/"+self.allFiles.item(i).text()
            print (temp)
            print (temp1)
            self.imgOriIndex=cv.imread(str(temp))
            self.modelIndex=cv.imread(str(temp1))
            img_temp1=copy.copy(self.imgOriIndex[:,:,0])
            img_temp2=copy.copy(self.modelIndex[:,:,0])
            img1=self.binary_img(img_org=img_temp1,thread=value_thread2)
            img2=self.binary_img(img_org=img_temp2,thread=value_thread2)
            self.img_contrastIndex=img1-img2
            img3=sm.opening(self.img_contrastIndex,sm.square(value_thread1))
            filepathtemp="QTGUIList/"+self.allFiles.item(i).text()
            height1=img3.shape[0]
            width1=img3.shape[1]
            count=0
            for i in range(height1):
                for j in range(width1):
                    if img3[i][j]!=0:
                        self.imgOriIndex[i][j][0]=255
                        self.imgOriIndex[i][j][1]=0
                        self.imgOriIndex[i][j][2]=0
                        count+=1
            print (count)        
            cv.imwrite(filepathtemp,self.imgOriIndex)
            objpath=QtGui.QPixmap(filepathtemp)
            pItem=QtWidgets.QListWidgetItem(QtGui.QIcon(objpath.scaled(QtCore.QSize(80,398))),filepathtemp)
            pItem.setSizeHint(QtCore.QSize(80,398))
            self.piclist.addItem(pItem)
        self.labelload.setText("load finished!")

    def img_visualize(self):
        dr=Figure_Canvas()
        dr.test()
        graphicscene=QtWidgets.QGraphicsScene()
        graphicscene.addWidget(dr)
        self.graphicview.setScene(graphicscene)
        self.graphicview.show()
        
        
    def sldvaluechange(self,value):
#        wtest=value
#        self.editX.setText(str(wtest))
#        radius=value/5
#        print (radius)
#        img_temp=copy.copy(self.imgOri)
#        a=range(int(350-radius),int(350+radius))
#        print (len(a))
#        b=range(int(80-radius),int(80+radius))
#        for i in a:
#            for j in b:
#                img_temp[i][j][0]=255
#                img_temp[i][j][1]=0
#                img_temp[i][j][2]=0
#        height=img_temp.shape[0]
#        ratioY=self.labelImg1.height()/(height+0.0)
#        
#        width=img_temp.shape[1]
#        height2=self.labelImg1.height()
#        width2=int(width*ratioY+0.5)
#        img4=cv.resize(img_temp,(width2,height2))
#        cv.imwrite("QTGUI/process003.png",img4)
#        cv.imwrite("QTGUI/process004.png",self.imgOri)
#        qImgT=QtGui.QPixmap("QTGUI/process003.png")
#        self.labelImg1.setPixmap(qImgT)
        
#        wtest=value/10.0
#        self.editW.setText(str(wtest))
#        dr=Figure_Canvas()
#        dr.test(w=wtest)
#        graphicscene=QtWidgets.QGraphicsScene()
#        graphicscene.addWidget(dr)
#        self.graphicview.setScene(graphicscene)
#        self.graphicview.show()
#        self.position1=value
#        ytest=self.position1
#        self.editX.setText(str(self.position1))
#        self.editY.setText(str(ytest))
#        dr=Figure_Canvas()
#        dr.test(X_line1=self.position1,X_line2=self.position2)
#        graphicscene=QtWidgets.QGraphicsScene()
#        graphicscene.addWidget(dr)
#        self.graphicview.setScene(graphicscene)
#        self.graphicview.show()
        self.position1=value
        ytest=int(self.position1/10)+1
        self.editX.setText(str(self.position1))
        self.editY.setText(str(ytest))
        dr=Figure_Canvas()
        dr.test(X_line1=self.position1)
        graphicscene=QtWidgets.QGraphicsScene()
        graphicscene.addWidget(dr)
        self.graphicview.setScene(graphicscene)
        self.graphicview.show()
        
        img3=sm.opening(self.img_contrast,sm.square(ytest))
        self.img_processed=copy.copy(self.imgOri)
        height1=img3.shape[0]
        width1=img3.shape[1]
        
        count=0
        for i in range(height1):
            for j in range(width1):
                if img3[i][j]!=0:
                    self.img_processed[i][j][0]=255
                    self.img_processed[i][j][1]=0
                    self.img_processed[i][j][2]=0
                    count+=1
        print (count)            
        height=self.img_processed.shape[0]
        ratioY=self.labelImg1.height()/(height+0.0)
        width=self.img_processed.shape[1]
        height2=self.labelImg1.height()
        width=int(width*ratioY+0.5)
        img2=cv.resize(self.img_processed,(width,height2))
        cv.imwrite("QTGUI/process004.png",img2)        
        qImgT1=QtGui.QPixmap("QTGUI/process004.png")
        self.labelImg1.setPixmap(qImgT1)

#     def sldvaluechange2(self,value):
#         self.position2=value
#         ytest=self.position2
#         self.editX1.setText(str(self.position2))
#         self.editY1.setText(str(ytest))
#         dr=Figure_Canvas()
#         dr.test(X_line1=self.position1,X_line2=self.position2)
#         graphicscene=QtWidgets.QGraphicsScene()
#         graphicscene.addWidget(dr)
#         self.graphicview.setScene(graphicscene)
#         self.graphicview.show()

        
        
if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    image_process=Image_Process()
    image_process.show()
    sys.exit(app.exec_())