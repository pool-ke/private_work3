# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 10:54:36 2017

@author: kWX491567
"""

import numpy as np
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QPalette,QFont
from PyQt5.QtWidgets import QRadioButton,QButtonGroup
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import os
import json
import math
import copy
import sys
import ctypes
from ctypes import *
import time
import cv2 as cv
import serial
import serial.tools.list_ports
from MvCamCtrlSDK import MvCamCtrlSDK
from PIL import ImageFilter
from PIL import Image
from pylab import *
import copy
import random
import skimage.morphology as sm
from skimage import filters
import time

gts = ctypes.windll.LoadLibrary('gts.dll')


class TJogPrm(Structure):
    _fields_ = [("acc", c_double),
                ("dec", c_double),
                ("smooth;", c_double)]


class TTrapPrm(Structure):
    _fields_ = [("acc", c_double),
                ("dec", c_double),
                ("velStart", c_double),
                ("smoothTime;", c_double)]


class myLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(myLabel, self).__init__(parent)

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            pointT = QMouseEvent.pos()
            motion_control.ROI_X = pointT.x()
            motion_control.ROI_Y = pointT.y()
            #        image_process.mouseprocess()

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            pointT = QMouseEvent.pos()
            motion_control.ROI_X_1 = pointT.x()
            motion_control.ROI_Y_1 = pointT.y()
            # motion_control.mouseprocess2()

            #    def mouseMoveEvent(self,QMouseEvent):
            #        pointT=QMouseEvent.pos()
            #        motion_control.ROI_X_2=pointT.x()
            #        motion_control.ROI_Y_2=pointT.y()
            #        motion_control.mouseprocess3()

    def wheelEvent(self, QMouseWheel):
        delta = QMouseWheel.angleDelta()
        print(delta.y())
        
class Figure_Canvas(FigureCanvas):
    def __init__(self, parent=None, width=3.4, height=2.3, dpi=100):

        fig = Figure(figsize=(width, height), dpi=100)
        fig.set_facecolor("#F5F5F5")
        fig.subplots_adjust(left=0.1,top=0.9,right=0.9,bottom=0.1)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        self.axes = fig.add_subplot(111)
        self.axes.set_xlim(1,16)
        self.axes.set_xlabel("X")
        self.axes.set_ylabel("Y")


    def show_curve(self,y_value):
        print (len(y_value))
        x = np.linspace(1, len(y_value),len(y_value),endpoint=True)
        print (x.shape)
        print (y_value.shape)
        self.axes.plot(x, y_value)


class Motion_Control(QtWidgets.QWidget):
    def __init__(self):
        super(Motion_Control, self).__init__()
        self.setGeometry(30, 30, 1000, 930)
        self.setWindowTitle("智能打光平台")

        self.ser1 = serial.Serial()
        self.ser1.port = 'COM1'

        self.ser1.baudrate = 19200
        self.ser1.bytesize = 8
        self.ser1.stopbits = 1
        self.ser1.parity = 'N'
        self.ser1.open()
        if (self.ser1.isOpen()):
            print("COM1打开成功")

        self.ser2 = serial.Serial()
        self.ser2.port = 'COM6'
        self.ser2.baudrate = 19200
        self.ser2.bytesize = 8
        self.ser2.stopbits = 1
        self.ser2.parity = 'N'
        self.ser2.open()
        if (self.ser2.isOpen()):
            print("COM6打开成功")

        self.ser3 = serial.Serial()
        self.ser3.port = 'COM7'
        self.ser3.baudrate = 19200
        self.ser3.bytesize = 8
        self.ser3.stopbits = 1
        self.ser3.parity = 'N'
        self.ser3.open()
        if (self.ser3.isOpen()):
            print("COM7打开成功")

        self.ser4 = serial.Serial()
        self.ser4.port = 'COM8'
        self.ser4.baudrate = 19200
        self.ser4.bytesize = 8
        self.ser4.stopbits = 1
        self.ser4.parity = 'N'
        self.ser4.open()
        if (self.ser4.isOpen()):
            print("COM8打开成功")

        self.ser5 = serial.Serial()
        self.ser5.port = 'COM9'
        self.ser5.baudrate = 19200
        self.ser5.bytesize = 8
        self.ser5.stopbits = 1
        self.ser5.parity = 'N'
        self.ser5.open()
        if (self.ser5.isOpen()):
            print("COM9打开成功")

        self.initUI()

        self.ROI_X = 0
        self.ROI_Y = 0
        self.ROI_X_1 = 0
        self.ROI_Y_1 = 0
        self.ROI_X_2 = 0
        self.ROI_Y_2 = 0
        self.Array_ROI = []
        self.ratio = 0
        self.ROI_H = 0
        self.ROI_W = 0
        self.imgOri = None
        self.testarray = []

        self.mvccsdks=None
        self.w = 0.8
        self.c1 = 1
        self.c2 = 1
        self.r1 = 0.3
        self.r2 = 0.3
        self.pN = 10
        self.max_iter = 3
        self.max_iter2=3
        self.dim = 5
        self.X = np.zeros((self.pN, self.dim))  # all the coordination and vertical of partical
        self.V = np.zeros((self.pN, self.dim))
        self.pbest = np.zeros((self.pN, self.dim))  # best coordination for individual and global
        self.gbest = np.zeros(self.dim)
        self.p_fit = np.zeros(self.pN)
        self.fit = 1e10
        self.target_array=[]
#        self.Array_ROI=[[144,240,98,192],[435,460,188,350],[456,484,282,346]]
        self.Array_ROI=[[144,236,93,181],[429,446,191,354],[447,470,285,354]]
#        self.Array_ROI=[]
        self.target_loss = []   #for the first iterator of the target function (by feng 29)
        self.ROI_weigth = [1, 1, 1]

    def initUI(self):

#        self.tabWidget = QtWidgets.QTabWidget(self)
#        self.tabWidget.move(20, 250)
#        self.tabWidget.resize(400, 160)
#        # Light1 including 4 channels
#        Light1Chan1 = QtWidgets.QLabel("Chan1")
#        self.Light1Chan1Edit = QtWidgets.QLineEdit()
#        Light1Chan1.setBuddy(self.Light1Chan1Edit)
#        Light1Chan2 = QtWidgets.QLabel("Chan2")
#        self.Light1Chan2Edit = QtWidgets.QLineEdit()
#        Light1Chan2.setBuddy(self.Light1Chan2Edit)
#        Light1Chan3 = QtWidgets.QLabel("Chan3")
#        self.Light1Chan3Edit = QtWidgets.QLineEdit()
#        Light1Chan3.setBuddy(self.Light1Chan3Edit)
#        Light1Chan4 = QtWidgets.QLabel("Chan4")
#        self.Light1Chan4Edit = QtWidgets.QLineEdit()
#        Light1Chan4.setBuddy(self.Light1Chan4Edit)
#        self.btnSetLight1 = QtWidgets.QPushButton(u"SetLight1", self)
#        self.btnSetLight1.clicked.connect(self.sendSerialLight1)
#
#        Light1Widget = QtWidgets.QWidget(self.tabWidget)
#        Light1Layout = QtWidgets.QGridLayout()
#        Light1Layout.addWidget(Light1Chan1, 0, 0)
#        Light1Layout.addWidget(self.Light1Chan1Edit, 0, 1)
#        Light1Layout.addWidget(Light1Chan2, 1, 0)
#        Light1Layout.addWidget(self.Light1Chan2Edit, 1, 1)
#        Light1Layout.addWidget(Light1Chan3, 2, 0)
#        Light1Layout.addWidget(self.Light1Chan3Edit, 2, 1)
#        Light1Layout.addWidget(Light1Chan4, 3, 0)
#        Light1Layout.addWidget(self.Light1Chan4Edit, 3, 1)
#        Light1Layout.addWidget(self.btnSetLight1, 0, 2, 1, 2)
#        Light1Widget.setLayout(Light1Layout)
#        self.tabWidget.addTab(Light1Widget, "Light1")
#
#        Light2Chan1 = QtWidgets.QLabel("Chan1")
#        self.Light2Chan1Edit = QtWidgets.QLineEdit()
#        Light2Chan1.setBuddy(self.Light1Chan1Edit)
#        Light2Chan2 = QtWidgets.QLabel("Chan2")
#        self.Light2Chan2Edit = QtWidgets.QLineEdit()
#        Light2Chan2.setBuddy(self.Light2Chan2Edit)
#        Light2Chan3 = QtWidgets.QLabel("Chan3")
#        self.Light2Chan3Edit = QtWidgets.QLineEdit()
#        Light2Chan3.setBuddy(self.Light2Chan3Edit)
#        Light2Chan4 = QtWidgets.QLabel("Chan4")
#        self.Light2Chan4Edit = QtWidgets.QLineEdit()
#        Light2Chan4.setBuddy(self.Light2Chan4Edit)
#        self.btnSetLight2 = QtWidgets.QPushButton(u"SetLight2", self)
#        self.btnSetLight2.clicked.connect(self.sendSerialLight2)
#        # Light2 layout
#        Light2Widget = QtWidgets.QWidget(self.tabWidget)
#        Light2Layout = QtWidgets.QGridLayout()
#        Light2Layout.addWidget(Light2Chan1, 0, 0)
#        Light2Layout.addWidget(self.Light2Chan1Edit, 0, 1)
#        Light2Layout.addWidget(Light2Chan2, 1, 0)
#        Light2Layout.addWidget(self.Light2Chan2Edit, 1, 1)
#        Light2Layout.addWidget(Light2Chan3, 2, 0)
#        Light2Layout.addWidget(self.Light2Chan3Edit, 2, 1)
#        Light2Layout.addWidget(Light2Chan4, 3, 0)
#        Light2Layout.addWidget(self.Light2Chan4Edit, 3, 1)
#        Light2Layout.addWidget(self.btnSetLight2, 0, 2, 3, 3)
#        Light2Widget.setLayout(Light2Layout)
#        self.tabWidget.addTab(Light2Widget, "Light2")
#
#        Light3Chan1 = QtWidgets.QLabel("Chan1")
#        self.Light3Chan1Edit = QtWidgets.QLineEdit()
#        Light3Chan1.setBuddy(self.Light3Chan1Edit)
#        Light3Chan2 = QtWidgets.QLabel("Chan2")
#        self.Light3Chan2Edit = QtWidgets.QLineEdit()
#        Light3Chan2.setBuddy(self.Light3Chan2Edit)
#        Light3Chan3 = QtWidgets.QLabel("Chan3")
#        self.Light3Chan3Edit = QtWidgets.QLineEdit()
#        Light3Chan3.setBuddy(self.Light3Chan3Edit)
#        Light3Chan4 = QtWidgets.QLabel("Chan4")
#        self.Light3Chan4Edit = QtWidgets.QLineEdit()
#        Light3Chan4.setBuddy(self.Light3Chan4Edit)
#        self.btnSetLight3 = QtWidgets.QPushButton(u"SetLight3", self)
#        self.btnSetLight3.clicked.connect(self.sendSerialLight3)
#        # Light3 layout
#        Light3Widget = QtWidgets.QWidget(self.tabWidget)
#        Light3Layout = QtWidgets.QGridLayout()
#        Light3Layout.addWidget(Light3Chan1, 0, 0)
#        Light3Layout.addWidget(self.Light3Chan1Edit, 0, 1)
#        Light3Layout.addWidget(Light3Chan2, 1, 0)
#        Light3Layout.addWidget(self.Light3Chan2Edit, 1, 1)
#        Light3Layout.addWidget(Light3Chan3, 2, 0)
#        Light3Layout.addWidget(self.Light3Chan3Edit, 2, 1)
#        Light3Layout.addWidget(Light3Chan4, 3, 0)
#        Light3Layout.addWidget(self.Light3Chan4Edit, 3, 1)
#        Light3Layout.addWidget(self.btnSetLight3, 0, 2, 3, 3)
#        Light3Widget.setLayout(Light3Layout)
#        self.tabWidget.addTab(Light3Widget, "Light3")
#
#        Light4Chan1 = QtWidgets.QLabel("Chan1")
#        self.Light4Chan1Edit = QtWidgets.QLineEdit()
#        Light4Chan1.setBuddy(self.Light4Chan1Edit)
#        Light4Chan2 = QtWidgets.QLabel("Chan2")
#        self.Light4Chan2Edit = QtWidgets.QLineEdit()
#        Light4Chan2.setBuddy(self.Light4Chan2Edit)
#        Light4Chan3 = QtWidgets.QLabel("Chan3")
#        self.Light4Chan3Edit = QtWidgets.QLineEdit()
#        Light4Chan3.setBuddy(self.Light4Chan3Edit)
#        Light4Chan4 = QtWidgets.QLabel("Chan4")
#        self.Light4Chan4Edit = QtWidgets.QLineEdit()
#        Light4Chan4.setBuddy(self.Light4Chan4Edit)
#        self.btnSetLight4 = QtWidgets.QPushButton(u"SetLight4", self)
#        self.btnSetLight4.clicked.connect(self.sendSerialLight4)
#        # Light4 layout
#        Light4Widget = QtWidgets.QWidget(self.tabWidget)
#        Light4Layout = QtWidgets.QGridLayout()
#        Light4Layout.addWidget(Light4Chan1, 0, 0)
#        Light4Layout.addWidget(self.Light4Chan1Edit, 0, 1)
#        Light4Layout.addWidget(Light4Chan2, 1, 0)
#        Light4Layout.addWidget(self.Light4Chan2Edit, 1, 1)
#        Light4Layout.addWidget(Light4Chan3, 2, 0)
#        Light4Layout.addWidget(self.Light4Chan3Edit, 2, 1)
#        Light4Layout.addWidget(Light4Chan4, 3, 0)
#        Light4Layout.addWidget(self.Light4Chan4Edit, 3, 1)
#        Light4Layout.addWidget(self.btnSetLight4, 0, 2, 3, 3)
#        Light4Widget.setLayout(Light4Layout)
#        self.tabWidget.addTab(Light4Widget, "Light4")
#
#        Light5Chan1 = QtWidgets.QLabel("Chan1")
#        self.Light5Chan1Edit = QtWidgets.QLineEdit()
#        Light5Chan1.setBuddy(self.Light5Chan1Edit)
#        Light5Chan2 = QtWidgets.QLabel("Chan2")
#        self.Light5Chan2Edit = QtWidgets.QLineEdit()
#        Light5Chan2.setBuddy(self.Light5Chan2Edit)
#        Light5Chan3 = QtWidgets.QLabel("Chan3")
#        self.Light5Chan3Edit = QtWidgets.QLineEdit()
#        Light5Chan3.setBuddy(self.Light5Chan3Edit)
#        Light5Chan4 = QtWidgets.QLabel("Chan4")
#        self.Light5Chan4Edit = QtWidgets.QLineEdit()
#        Light5Chan4.setBuddy(self.Light5Chan4Edit)
#        self.btnSetLight5 = QtWidgets.QPushButton(u"SetLight5", self)
#        self.btnSetLight5.clicked.connect(self.sendSerialLight5)
#        # Light5 layout
#        Light5Widget = QtWidgets.QWidget(self.tabWidget)
#        Light5Layout = QtWidgets.QGridLayout()
#        Light5Layout.addWidget(Light5Chan1, 0, 0)
#        Light5Layout.addWidget(self.Light5Chan1Edit, 0, 1)
#        Light5Layout.addWidget(Light5Chan2, 1, 0)
#        Light5Layout.addWidget(self.Light5Chan2Edit, 1, 1)
#        Light5Layout.addWidget(Light5Chan3, 2, 0)
#        Light5Layout.addWidget(self.Light5Chan3Edit, 2, 1)
#        Light5Layout.addWidget(Light5Chan4, 3, 0)
#        Light5Layout.addWidget(self.Light5Chan4Edit, 3, 1)
#        Light5Layout.addWidget(self.btnSetLight5, 0, 2, 3, 3)
#        Light5Widget.setLayout(Light5Layout)
#        self.tabWidget.addTab(Light5Widget, "Light5")
        
        

#        self.btnGetCamera = QtWidgets.QPushButton(u"触发拍照", self)
#        self.btnGetCamera.move(50, 520)
#        self.btnGetCamera.clicked.connect(self.get_Camera_image)
        self.labelImg5 = QtWidgets.QLabel(self)
        self.labelImg5.move(65, 20)
        self.labelImg5.resize(850, 108)
        
        self.labelImg1 = myLabel(self)
        self.labelImg1.setAlignment(Qt.AlignTop)  # self.labelImg1.setAlignment(Qt.AlignCenter)  # AlignTop
        pe = QPalette()
        self.labelImg1.setAutoFillBackground(True)
        pe.setColor(QPalette.Window, Qt.gray)
        self.labelImg1.setPalette(pe)
        self.labelImg1.move(30, 180)
        self.labelImg1.resize(550, 400)
        
        self.labelImg2 = QtWidgets.QLabel(self)
        self.labelImg2.setAlignment(Qt.AlignCenter)  # self.labelImg1.setAlignment(Qt.AlignCenter)  # AlignTop
        pe = QPalette()
        self.labelImg2.setAutoFillBackground(True)
        pe.setColor(QPalette.Window, Qt.gray)
        self.labelImg2.setPalette(pe)
        self.labelImg2.move(30, 650)
        self.labelImg2.resize(300, 270)
        
        self.labelImg3 = QtWidgets.QLabel(self)
        self.labelImg3.setAlignment(Qt.AlignCenter)  # self.labelImg1.setAlignment(Qt.AlignCenter)  # AlignTop
        pe = QPalette()
        self.labelImg3.setAutoFillBackground(True)
        pe.setColor(QPalette.Window, Qt.gray)
        self.labelImg3.setPalette(pe)
        self.labelImg3.move(355, 650)
        self.labelImg3.resize(300, 270)
        
        self.labelImg4 = QtWidgets.QLabel(self)
        self.labelImg4.setAlignment(Qt.AlignCenter)  # self.labelImg1.setAlignment(Qt.AlignCenter)  # AlignTop
        pe = QPalette()
        self.labelImg4.setAutoFillBackground(True)
        pe.setColor(QPalette.Window, Qt.gray)
        self.labelImg4.setPalette(pe)
        self.labelImg4.move(680, 650)
        self.labelImg4.resize(300, 270)
        
        self.labeltext1 = QtWidgets.QLabel("全图:", self)
        self.labeltext1.move(30, 150)
        self.labeltext1.setFont(QFont("Roman times",15,QFont.Bold))
#        
        self.labeltext2 = QtWidgets.QLabel("感兴趣区域一:", self)
        self.labeltext2.move(30, 620)
        self.labeltext2.setFont(QFont("Roman times",15,QFont.Bold))
#        
        self.labeltext3 = QtWidgets.QLabel("感兴趣区域二:", self)
        self.labeltext3.move(355, 620)
        self.labeltext3.setFont(QFont("Roman times",15,QFont.Bold))
#        
        self.labeltext4 = QtWidgets.QLabel("感兴趣区域三:", self)
        self.labeltext4.move(680, 620)
        self.labeltext4.setFont(QFont("Roman times",15,QFont.Bold))
#        
#        self.labeltext5 = QtWidgets.QLabel("迭代曲线:", self)
#        self.labeltext5.move(820, 150)
#        self.labeltext5.setFont(QFont("Roman times",15,QFont.Bold))
        
        self.graphicview = QtWidgets.QGraphicsView(self)
        self.graphicview.move(620, 340)
        self.graphicview.resize(360, 240)

#        self.labelX1 = QtWidgets.QLabel(u"X1:", self)
#        self.labelX1.move(20, 20)
#        self.editX1 = QtWidgets.QLineEdit(self)
#        self.editX1.move(50, 18)
#        self.editX1.resize(40, 20)
#        self.editX1.setText("0")
#
#        self.labelA1 = QtWidgets.QLabel(u"A1:", self)
#        self.labelA1.move(100, 20)
#        self.editA1 = QtWidgets.QLineEdit(self)
#        self.editA1.move(130, 18)
#        self.editA1.resize(40, 20)
#        self.editA1.setText("0")
#
#        self.labelZ1 = QtWidgets.QLabel(u"Z1:", self)
#        self.labelZ1.move(180, 20)
#        self.editZ1 = QtWidgets.QLineEdit(self)
#        self.editZ1.move(210, 18)
#        self.editZ1.resize(40, 20)
#        self.editZ1.setText("0")
#
#        self.labelX2 = QtWidgets.QLabel(u"X2:", self)
#        self.labelX2.move(20, 50)
#        self.editX2 = QtWidgets.QLineEdit(self)
#        self.editX2.move(50, 48)
#        self.editX2.resize(40, 20)
#        self.editX2.setText("0")
#
#        self.labelA2 = QtWidgets.QLabel(u"A2:", self)
#        self.labelA2.move(100, 50)
#        self.editA2 = QtWidgets.QLineEdit(self)
#        self.editA2.move(130, 48)
#        self.editA2.resize(40, 20)
#        self.editA2.setText("0")
#
#        self.labelZ2 = QtWidgets.QLabel(u"Z2:", self)
#        self.labelZ2.move(180, 50)
#        self.editZ2 = QtWidgets.QLineEdit(self)
#        self.editZ2.move(210, 48)
#        self.editZ2.resize(40, 20)
#        self.editZ2.setText("0")

        self.labelX3 = QtWidgets.QLabel("水平轴:", self)
#        self.labelX3.move(20, 80)
        self.editX3 = QtWidgets.QLineEdit(self)
#        self.editX3.move(50, 78)
#        self.editX3.resize(40, 20)
#        self.editX3.setText("0")

        self.labelA3 = QtWidgets.QLabel("旋转轴:", self)
#        self.labelA3.move(100, 80)
        self.editA3 = QtWidgets.QLineEdit(self)
#        self.editA3.move(130, 78)
#        self.editA3.resize(40, 20)
#        self.editA3.setText("0")

        self.labelZ3 = QtWidgets.QLabel("垂直轴:", self)
#        self.labelZ3.move(180, 80)
        self.editZ3 = QtWidgets.QLineEdit(self)
#        self.editZ3.move(210, 78)
#        self.editZ3.resize(40, 20)
#        self.editZ3.setText("0")

#        self.labelX4 = QtWidgets.QLabel(u"X4:", self)
#        self.labelX4.move(20, 110)
#        self.editX4 = QtWidgets.QLineEdit(self)
#        self.editX4.move(50, 108)
#        self.editX4.resize(40, 20)
#        self.editX4.setText("0")
#
#        self.labelA4 = QtWidgets.QLabel(u"A4:", self)
#        self.labelA4.move(100, 110)
#        self.editA4 = QtWidgets.QLineEdit(self)
#        self.editA4.move(130, 108)
#        self.editA4.resize(40, 20)
#        self.editA4.setText("0")
#
#        self.labelZ4 = QtWidgets.QLabel(u"Z4:", self)
#        self.labelZ4.move(180, 110)
#        self.editZ4 = QtWidgets.QLineEdit(self)
#        self.editZ4.move(210, 108)
#        self.editZ4.resize(40, 20)
#        self.editZ4.setText("0")

#        self.labeltext = QtWidgets.QLabel(u"init", self)
#        self.labeltext.move(20, 180)
        
#        self.labeltext2 = QtWidgets.QLabel("控制轴号：",self)

#        self.labelY = QtWidgets.QLabel(u"Y:", self)
#        self.labelY.move(20, 140)
#        self.editY = QtWidgets.QLineEdit(self)
#        self.editY.move(50, 138)
#        self.editY.resize(40, 20)
#        self.editY.setText("0")

#        self.labelZ = QtWidgets.QLabel(u"Z:", self)
#        self.labelZ.move(100, 140)
#        self.editZ = QtWidgets.QLineEdit(self)
#        self.editZ.move(130, 138)
#        self.editZ.resize(40, 20)
#        self.editZ.setText("0")

        self.label_exposure_time = QtWidgets.QLabel(u"曝光度:", self)
#        self.label_exposure_time.move(180, 140)
        self.edit_exposure_time = QtWidgets.QLineEdit(self)
#        self.edit_exposure_time.move(210, 138)
#        self.edit_exposure_time.resize(40, 20)
        self.edit_exposure_time.setText("4000.0")

        self.buttonMove = QtWidgets.QPushButton("初始化粒子", self)
        self.buttonMove.move(900,260)
        self.buttonMove.clicked.connect(self.fun_move)

#        self.buttonTakePhoto = QtWidgets.QPushButton(u"Take Photo", self)
#        self.buttonTakePhoto.move(300, 50)
#        self.buttonTakePhoto.clicked.connect(self.fun_takephoto)

#        self.editAxis = QtWidgets.QLineEdit(self)
#        self.editAxis.resize(50, 20)
#        self.editAxis.setText("X3")

        self.buttonLink = QtWidgets.QPushButton("启动设备", self)
        self.buttonLink.move(900, 200)
        self.buttonLink.clicked.connect(self.connect_link)

        self.buttonUnLink = QtWidgets.QPushButton(u"关闭设备", self)
        self.buttonUnLink.move(900, 230)
        self.buttonUnLink.clicked.connect(self.connect_unlink)

#        self.buttonMoveUp = QtWidgets.QPushButton(u"前进", self)
##        self.buttonMoveUp.move(450, 80)
#        self.buttonMoveUp.pressed.connect(self.move_up)
#        self.buttonMoveUp.released.connect(self.move_stop)
#
#        self.buttonMoveDown = QtWidgets.QPushButton(u"后退", self)
##        self.buttonMoveUp.move(450, 110)
#        self.buttonMoveDown.pressed.connect(self.move_down)
#        self.buttonMoveDown.released.connect(self.move_stop)
#
#        self.buttonReset = QtWidgets.QPushButton(u"复位", self)
##        self.buttonReset.move(450, 140)
#        self.buttonReset.clicked.connect(self.reset)
#
#        self.buttonGetsts = QtWidgets.QPushButton(u"获取状态", self)
##        self.buttonGetsts.move(450, 170)
#        self.buttonGetsts.clicked.connect(self.move_getsts)
#
#        self.buttonclrsts = QtWidgets.QPushButton(u"清除限位", self)
##        self.buttonclrsts.move(450, 200)
#        self.buttonclrsts.clicked.connect(self.move_clrsts)

#        self.buttonAutoAcquireData = QtWidgets.QPushButton(u"Auto", self)
#        self.buttonAutoAcquireData.move(450, 230)
#        self.buttonAutoAcquireData.clicked.connect(self.AutoAcquireData)

        self.buttonGenerateTestArray = QtWidgets.QPushButton(u"优化计算", self)
        self.buttonGenerateTestArray.move(900, 290)
        self.buttonGenerateTestArray.clicked.connect(self.GenerateTestArray)
        
        self.labeltext5=QtWidgets.QLabel(self)
        self.labeltext5.setText("产品选择：")
        self.labeltext5.move(900,150)
        
        self.comboxproduct=QtWidgets.QComboBox(self)
        self.comboxproduct.move(900,170)
        
        self.comboxproduct.addItem("种类一")
        self.comboxproduct.addItem("种类二")
        self.comboxproduct.addItem("种类三")
        
        self.comboxproduct.currentIndexChanged.connect(self.fun_combox)

#        self.buttonInit = QtWidgets.QPushButton(u"InitPSO", self)
#        self.buttonInit.move(450, 290)
#        self.buttonInit.clicked.connect(self.init_Population)

#        self.buttonIter = QtWidgets.QPushButton(u"Iterator", self)
#        self.buttonIter.move(450, 320)
#        self.buttonIter.clicked.connect(self.Iterator)

#        self.buttonMovetoBest = QtWidgets.QPushButton(u"保存最优图片", self)
#        self.buttonMovetoBest.move(450, 140)
#        self.buttonMovetoBest.clicked.connect(self.move_to_best)

#        self.buttonSendWL = QtWidgets.QPushButton(u"拍照位", self)
##        self.buttonSendWL.move(450, 380)
#        self.buttonSendWL.clicked.connect(self.SendWL)
#
#        self.buttonReturnWL = QtWidgets.QPushButton(u"物料位", self)
##        self.buttonReturnWL.move(450, 410)
#        self.buttonReturnWL.clicked.connect(self.ReturnWL)

#        self.buttonSetLigiht = QtWidgets.QPushButton(u"设置光照", self)
#        self.buttonSetLigiht.move(450, 140)
#        self.buttonSetLigiht.clicked.connect(self.SetLight)
#
#        self.buttonAddROI = QtWidgets.QPushButton(u"添加ROI", self)
#        self.buttonAddROI.move(130, 520)
#        self.buttonAddROI.clicked.connect(self.AddROI)
#
#        self.buttonPrintROI = QtWidgets.QPushButton(u"ROI信息", self)
#        self.buttonPrintROI.move(210, 520)
#        self.buttonPrintROI.clicked.connect(self.PrintROI)
        
#        self.buttonLinkCam = QtWidgets.QPushButton(u"连接相机", self)
#        self.buttonLinkCam.clicked.connect(self.Linkcamera)
#        
#        self.buttonUnLinkCam = QtWidgets.QPushButton(u"断开相机", self)
#        self.buttonUnLinkCam.clicked.connect(self.UnLinkcamera)
        
#        self.buttonIter2 = QtWidgets.QPushButton(u"Iterator2", self)
#        self.buttonIter2.move(450, 590)
#        self.buttonIter2.clicked.connect(self.Iterator2)
        
#        self.buttonSave = QtWidgets.QPushButton(u"SaveTxt", self)
#        self.buttonSave.move(450, 620)
#        self.buttonSave.clicked.connect(self.SaveTxt)
        
#        self.rb11 = QRadioButton('相机一',self)
#        self.rb12 = QRadioButton('相机二',self)
#        self.rb12.setChecked(1)
#        self.rb13 = QRadioButton('相机三', self)
#        
#        self.bg1 = QButtonGroup(self)
#        self.bg1.addButton(self.rb11,1)
#        self.bg1.addButton(self.rb12,2)
#        self.bg1.addButton(self.rb13,3)
#        
#        self.radioWidget = QtWidgets.QTabWidget(self)
#        self.radioWidget.move(550, 20)
#        self.radioWidget.resize(150, 160)
#        
#        CameraWidget = QtWidgets.QWidget(self.radioWidget)
#        CameraLayout = QtWidgets.QGridLayout()
#        CameraLayout.addWidget(self.rb11, 0, 0)
#        CameraLayout.addWidget(self.rb12, 1, 0)
#        CameraLayout.addWidget(self.rb13, 2, 0)
#        CameraLayout.addWidget(self.buttonLinkCam,1,1)
#        CameraLayout.addWidget(self.buttonUnLinkCam,2,1)
#        self.radioWidget.setLayout(CameraLayout)
#        self.radioWidget.addTab(CameraWidget, "相机选择")
#
#        
#        self.axisWidget=QtWidgets.QTabWidget(self)
#        self.axisWidget.move(550,200)
#        self.axisWidget.resize(150,220)
#        
#        
#        
#        AxisWidget=QtWidgets.QWidget(self.axisWidget)
#        AxisLayout=QtWidgets.QGridLayout()
#        AxisLayout.addWidget(self.labeltext2,0,0)
#        AxisLayout.addWidget(self.editAxis,0,1)
#        AxisLayout.addWidget(self.buttonMoveUp,1,0)
#        AxisLayout.addWidget(self.buttonMoveDown,2,0)
#        AxisLayout.addWidget(self.buttonReset,3,0)
#        AxisLayout.addWidget(self.buttonGetsts,1,1)
#        AxisLayout.addWidget(self.buttonclrsts,2,1)
#        AxisLayout.addWidget(self.buttonSendWL,4,0)
#        AxisLayout.addWidget(self.buttonReturnWL,4,1)
#        self.axisWidget.setLayout(AxisLayout)
#        self.axisWidget.addTab(AxisWidget,"单轴控制")
        
        self.paraWidget=QtWidgets.QTabWidget(self)
        self.paraWidget.move(620,180)
        self.paraWidget.resize(250,150)
        
        Light1Chan1 = QtWidgets.QLabel("光源一：")
        self.Light1Chan1Edit = QtWidgets.QLineEdit()
        Light2Chan3 = QtWidgets.QLabel("光源二：")
        self.Light2Chan3Edit = QtWidgets.QLineEdit()
        
        
        ParaWidget=QtWidgets.QWidget(self.paraWidget)
        ParaLayout=QtWidgets.QGridLayout()
        ParaLayout.addWidget(self.labelX3,0,0)     
        ParaLayout.addWidget(self.editX3,0,1)
        ParaLayout.addWidget(self.labelZ3,1,0)     
        ParaLayout.addWidget(self.editZ3,1,1)
        ParaLayout.addWidget(self.labelA3,2,0)     
        ParaLayout.addWidget(self.editA3,2,1)
        ParaLayout.addWidget(Light1Chan1,0,2)
        ParaLayout.addWidget(self.Light1Chan1Edit,0,3)
        ParaLayout.addWidget(Light2Chan3,1,2)
        ParaLayout.addWidget(self.Light2Chan3Edit,1,3)
        ParaLayout.addWidget(self.label_exposure_time,2,2)
        ParaLayout.addWidget(self.edit_exposure_time,2,3)
        self.paraWidget.setLayout(ParaLayout)
        self.paraWidget.addTab(ParaWidget,"待优化参数")
        
        self.editX3.setText("33")
        self.editZ3.setText("0")
        self.editA3.setText("-55")
        self.Light1Chan1Edit.setText("80")
        self.Light2Chan3Edit.setText("150")
        
        self.Load_Logo()
        
        dr = Figure_Canvas()
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(dr)
        self.graphicview.setScene(graphicscene)
        self.graphicview.show()
    def mouseprocess2(self):
        print(self.ROI_X_1)
        print(self.ROI_Y_1)
        positionX = int(self.ROI_X / self.ratio)
        positionY = int(self.ROI_Y / self.ratio)
        print(positionX)
        print(positionY)
        self.ROI_W = int(self.ROI_X_1 / self.ratio) - int(self.ROI_X / self.ratio)
        self.ROI_H = int(self.ROI_Y_1 / self.ratio) - int(self.ROI_Y / self.ratio)
        print(self.ROI_W)
        print(self.ROI_H)

        self.imgLabel = copy.copy(self.imgOri[:, :])
        cv.imwrite("QTGUI_Label/process003.png", self.imgOri)
        #        cv.line(self.imgLabel,(int(self.ROI_X/self.ratio),int(self.ROI_Y/self.ratio)),(int(self.ROI_X_1/self.ratio),int(self.ROI_Y_1/self.ratio)),(255,0,0),5)
        cv.rectangle(self.imgLabel, (int(self.ROI_X / self.ratio), int(self.ROI_Y / self.ratio)),
                     (int(self.ROI_X_1 / self.ratio), int(self.ROI_Y_1 / self.ratio)), (0, 0, 255), 5)
        cv.imwrite("QTGUI_Label/process001.png", self.imgLabel)
        #        image_tmp=cv.imread('a.QTGUI_Label/process001.png', 0)
        #        img2=self.picture_resize(imgOri=image_tmp,Label=self.labelImg1)
        #        cv.imwrite("QTGUI_Label/process001.png",img2)
        #        qImgT1=QtGui.QPixmap("QTGUI_Label/process001.png")
        #        self.labelImg1.setPixmap(qImgT1)
        self.img_processed = copy.copy(self.imgOri[int(self.ROI_Y / self.ratio):int(self.ROI_Y_1 / self.ratio),
                                       int(self.ROI_X / self.ratio):int(self.ROI_X_1 / self.ratio)])
        cv.imwrite("QTGUI_Label/process005.png", self.img_processed)

    #    def mouseprocess3(self):
    #        print (self.ROI_X_2)
    #        print (self.ROI_Y_2)
    #        self.ROI_W=int(self.ROI_X_2/self.ratio)-int(self.ROI_X/self.ratio)
    #        self.ROI_H=int(self.ROI_Y_2/self.ratio)-int(self.ROI_Y/self.ratio)
    #        print (self.ROI_W)
    #        print (self.ROI_H)
    #        self.imgLabel1=copy.copy(self.imgOri[:,:])
    #        cv.rectangle(self.imgLabel1,(int(self.ROI_X/self.ratio),int(self.ROI_Y/self.ratio)),(int(self.ROI_X_2/self.ratio),int(self.ROI_Y_2/self.ratio)),(255,0,0),5)
    ##        img2=self.picture_resize(imgOri=self.imgLabel1,Label=self.labelImg1)
    ##        cv.imwrite("QTGUI_Label/process001.png",img2)
    ##        qImgT1=QtGui.QPixmap("QTGUI_Label/process001.png")
    ##        self.labelImg1.setPixmap(qImgT1)
    #        cv.imwrite("QTGUI_Label/process004.png",self.imgLabel)
    ##        if (self.drawing):
    ##            print ("111")
    ##        else:
    ##            print ("222")


    def gts_p2p(self, axis, position):
        pos = c_long(int(position))
        vel = c_double(float(10))
        # print "p2p(axis=%d,pos=%d,vel=%.2f,acc=%.2f)" % (axis,pos,vel,acc)
        print("p2p")
        p2p = TTrapPrm()
        p2p.acc = 0.25
        p2p.dec = 0.125
        p2p.smoothTime = 25
        p2p.velStart = 0
        print("my_PrfJog", gts.GT_PrfTrap(axis))
        print("my_SetTrapPrm", gts.GT_SetTrapPrm(axis, byref(p2p)))
        print("my_SetVel", gts.GT_SetVel(axis, vel))
        print("my_SetPos", gts.GT_SetPos(axis, pos.value))
        print("my_Update", gts.GT_Update(1 << axis - 1))

    def gts_jog(self, axis, dir):
        vel = c_double(float(2))
        # print "p2p(axis=%d,pos=%d,vel=%.2f,acc=%.2f)" % (axis,pos,vel,acc)
        print("JOG")
        jog = TJogPrm()
        jog.acc = 0.25
        jog.dec = 0.125
        jog.smooth = 0.5
        print("my_PrfJog", gts.GT_PrfJog(axis))
        print("my_SetJogPrm", gts.GT_SetJogPrm(axis, byref(jog)))
        print("my_SetVel", gts.GT_SetVel(axis, c_double(vel.value * dir)))
        print("my_Update", gts.GT_Update(1 << axis - 1))

    def connect_link(self):
        print("GT_SetCardNo():", gts.GT_SetCardNo(c_short(0)))
        print("GT_Open_Card1()=", gts.GT_Open(c_short(0), c_short(1)))
        # print("GT_Reset():",gts.GT_Reset(0))
        print("GT_AxisOn():", gts.GT_AxisOn(c_short(1)))
        print("GT_AxisOn():", gts.GT_AxisOn(c_short(2)))
        print("GT_AxisOn():", gts.GT_AxisOn(c_short(3)))
        print("GT_AxisOn():", gts.GT_AxisOn(c_short(4)))
        print("GT_AxisOn():", gts.GT_AxisOn(c_short(5)))
        print("GT_AxisOn():", gts.GT_AxisOn(c_short(6)))
        print("GT_AxisOn():", gts.GT_AxisOn(c_short(7)))
        print("GT_AxisOn():", gts.GT_AxisOn(c_short(8)))
        print("GT_SetCardNo():", gts.GT_SetCardNo(c_short(1)))
        print("GT_Open_Card2()=", gts.GT_Open(c_short(0), c_short(1)))
        print("GT_AxisOn():", gts.GT_AxisOn(c_short(1)))
        print("GT_AxisOn():", gts.GT_AxisOn(c_short(2)))
        print("GT_AxisOn():", gts.GT_AxisOn(c_short(3)))
        print("GT_AxisOn():", gts.GT_AxisOn(c_short(4)))
        print("GT_AxisOn():", gts.GT_AxisOn(c_short(5)))
        print("GT_AxisOn():", gts.GT_AxisOn(c_short(6)))
        
        self.Linkcamera()
#        self.labeltext.setText("GT_Open")

    def connect_unlink(self):
        self.ReturnWL()
        time.sleep(3)
        print("GT_SetCardNo():", gts.GT_SetCardNo(c_short(1)))
        print("GT_AxisOff():", gts.GT_AxisOff(c_short(1)))
        print("GT_AxisOff():", gts.GT_AxisOff(c_short(2)))
        print("GT_AxisOff():", gts.GT_AxisOff(c_short(3)))
        print("GT_AxisOff():", gts.GT_AxisOff(c_short(4)))
        print("GT_AxisOff():", gts.GT_AxisOff(c_short(5)))
        print("GT_AxisOff():", gts.GT_AxisOff(c_short(6)))
        print("GT_Close_Card1():", gts.GT_Close())
        print("GT_SetCardNo():", gts.GT_SetCardNo(c_short(0)))
        print("GT_AxisOff():", gts.GT_AxisOff(c_short(1)))
        print("GT_AxisOff():", gts.GT_AxisOff(c_short(2)))
        print("GT_AxisOff():", gts.GT_AxisOff(c_short(3)))
        print("GT_AxisOff():", gts.GT_AxisOff(c_short(4)))
        print("GT_AxisOff():", gts.GT_AxisOff(c_short(5)))
        print("GT_AxisOff():", gts.GT_AxisOff(c_short(6)))
        print("GT_AxisOff():", gts.GT_AxisOff(c_short(7)))
        print("GT_AxisOff():", gts.GT_AxisOff(c_short(8)))
        print("GT_Close_Card2():", gts.GT_Close())
        self.UnLinkcamera()
        self.sendSerialLight1_V2(brightness_light1='000')
        self.sendSerialLight2_V2(brightness_light2='000')
#        self.labeltext.setText("GT_Close")

    def fun_move(self):
        #        position_X1 = int(self.editX1.text())
        # position_Z1 = int(self.editZ1.text())
        #        position_A1 = int(self.editA1.text())
        #        position_X2 = int(self.editX2.text())
        #        position_Z2 = int(self.editZ2.text())
        #        position_A2 = int(self.editA2.text())
        # position_X3 = int(self.editX3.text())
        # position_Z3 = int(self.editZ3.text())
        # position_A3 = int(self.editA3.text())
        #        position_X4 = int(self.editX4.text())
        #        position_Z4 = int(self.editZ4.text())
        #        position_A4 = int(self.editA4.text())
        # position_Y = int(self.editY.text())
        # position_Z = int(self.editZ.text())
#        position_Z1 = float(self.editZ1.text())
        self.SendWL()
        position_X3 = float(self.editX3.text())
        position_Z3 = float(self.editZ3.text())
        position_A3 = float(self.editA3.text())
#        position_Y = float(self.editY.text())
#        position_Z = float(self.editZ.text())
#        print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(0)))
#        #        self.gts_p2p(1,position_X1)
#        self.gts_p2p(2, position_Z1 * 2000)
#        #        self.gts_p2p(3, position_A1)
#        self.gts_p2p(4, position_Y * 2000)
#        self.gts_p2p(5, position_Z * 2000)
        print("GT_SetCardNo_Card2():", gts.GT_SetCardNo(c_short(1)))
        self.gts_p2p(1, position_X3 * 200)
        self.gts_p2p(2, position_Z3 * 200)
        self.gts_p2p(3, position_A3 * 200)
        self.SetLight()
        #        self.gts_p2p(6, position_X2)
        #        self.gts_p2p(7, position_Z2)
        #        self.gts_p2p(8, position_A2)
        #        print("GT_SetCardNo_Card2():", gts.GT_SetCardNo(c_short(1)))
        #        self.gts_p2p(1, position_X3)
        #        self.gts_p2p(2, position_Z3)
        #        self.gts_p2p(3, position_A3)
        #        self.gts_p2p(4, position_X4)
        #        self.gts_p2p(5, position_Z4)
        #        self.gts_p2p(6, position_A4)



    def move_to_destination(self, position_X3, position_Z3, position_A3):
        print("GT_SetCardNo_Card2():", gts.GT_SetCardNo(c_short(1)))
        self.gts_p2p(1, position_X3)
        self.gts_p2p(2, position_Z3)
        self.gts_p2p(3, position_A3)
        print("GT_ClrSts():", gts.GT_ClrSts(c_short(1), c_short(1)))
        print("GT_ClrSts():", gts.GT_ClrSts(c_short(2), c_short(1)))
        print("GT_ClrSts():", gts.GT_ClrSts(c_short(3), c_short(1)))

    def move_up(self):
        axis_adjust = self.editAxis.text()
        position = c_double()
        clock = c_ulong()
        if (axis_adjust == "Z1"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(0)))
            self.gts_jog(2, -1)
        elif (axis_adjust == "Y"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(0)))
            self.gts_jog(4, -1)
        elif (axis_adjust == "Z"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(0)))
            self.gts_jog(5, -1)
        elif (axis_adjust == "X3"):
            print("GT_SetCardNo_Card2():", gts.GT_SetCardNo(c_short(1)))
            self.gts_jog(1, -1)
        elif (axis_adjust == "Z3"):
            print("GT_SetCardNo_Card2():", gts.GT_SetCardNo(c_short(1)))
            self.gts_jog(2, -1)
        elif (axis_adjust == "A3"):
            print("GT_SetCardNo_Card2():", gts.GT_SetCardNo(c_short(1)))
            self.gts_jog(3, -1)
        else:
            print("please input the axis.")

    def move_stop(self):
        axis_adjust = self.editAxis.text()
        print(axis_adjust)
        if (axis_adjust == "Z1"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(0)))
            print('GT_Stop', gts.GT_Stop(c_long(0xff), c_long(0xff)))
            position = c_double()
            clock = c_ulong()
            print("GT_GetPosition():", gts.GT_GetPrfPos(c_short(2), byref(position), c_short(1), byref(clock)))
            position_Z1 = position.value / 2000
            self.editZ1.setText('%.3f' % position_Z1)
            # self.editZ1.setText(str(position.value/2000))
        elif (axis_adjust == "Y"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(0)))
            print('GT_Stop', gts.GT_Stop(c_long(0xff), c_long(0xff)))
            position = c_double()
            clock = c_ulong()
            print("GT_GetPosition():", gts.GT_GetPrfPos(c_short(4), byref(position), c_short(1), byref(clock)))
            position_Y = position.value / 2000
            self.editY.setText('%.3f' % position_Y)
            # self.editY.setText(str(position.value))
        elif (axis_adjust == "Z"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(0)))
            print('GT_Stop', gts.GT_Stop(c_long(0xff), c_long(0xff)))
            position = c_double()
            clock = c_ulong()
            print("GT_GetPosition():", gts.GT_GetPrfPos(c_short(5), byref(position), c_short(1), byref(clock)))
            position_Z = position.value / 2000
            self.editZ.setText('%.3f' % position_Z)
            # self.editZ.setText(str(position.value))
        elif (axis_adjust == "X3"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(1)))
            print('GT_Stop', gts.GT_Stop(c_long(0xff), c_long(0xff)))
            position = c_double()
            clock = c_ulong()
            print("GT_GetPosition():", gts.GT_GetPrfPos(c_short(1), byref(position), c_short(1), byref(clock)))
            position_X3 = position.value / 200
            self.editX3.setText('%.3f' % position_X3)
            # self.editX3.setText(str(position.value))
        elif (axis_adjust == "Z3"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(1)))
            print('GT_Stop', gts.GT_Stop(c_long(0xff), c_long(0xff)))
            position = c_double()
            clock = c_ulong()
            print("GT_GetPosition():", gts.GT_GetPrfPos(c_short(2), byref(position), c_short(1), byref(clock)))
            position_Z3 = position.value / 200
            self.editZ3.setText('%.3f' % position_Z3)
            # self.editZ3.setText(str(position.value))
        elif (axis_adjust == "A3"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(1)))
            print('GT_Stop', gts.GT_Stop(c_long(0xff), c_long(0xff)))
            position = c_double()
            clock = c_ulong()
            print("GT_GetPosition():", gts.GT_GetPrfPos(c_short(3), byref(position), c_short(1), byref(clock)))
            position_A3 = position.value / 200
            self.editA3.setText('%.3f' % position_A3)
            # self.editA3.setText(str(position.value))
        else:
            print("please input the axis.")

    def move_down(self):
        axis_adjust = self.editAxis.text()
        if (axis_adjust == "Z1"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(0)))
            self.gts_jog(2, 1)
        elif (axis_adjust == "Y"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(0)))
            self.gts_jog(4, 1)
        elif (axis_adjust == "Z"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(0)))
            self.gts_jog(5, 1)
        elif (axis_adjust == "X3"):
            print("GT_SetCardNo_Card2():", gts.GT_SetCardNo(c_short(1)))
            self.gts_jog(1, 1)
        elif (axis_adjust == "Z3"):
            print("GT_SetCardNo_Card2():", gts.GT_SetCardNo(c_short(1)))
            self.gts_jog(2, 1)
        elif (axis_adjust == "A3"):
            print("GT_SetCardNo_Card2():", gts.GT_SetCardNo(c_short(1)))
            self.gts_jog(3, 1)
        else:
            print("please input the axis.")

    def homeback(self, axis_move):
        pos = c_long(int(-50000000))
        vel = c_double(float(3))
        acc = c_double(float(0.25))
        dec = c_double(float(0.125))
        smooth = c_double(float(25))
        p2p = TTrapPrm()
        p2p.acc = acc
        p2p.dec = dec
        p2p.smoothTime = smooth
        p2p.velStart = 0
        print("my_PrfJog", gts.GT_PrfTrap(c_short(axis_move)))
        print("my_SetTrapPrm", gts.GT_SetTrapPrm(c_short(axis_move), byref(p2p)))
        print("my_SetVel", gts.GT_SetVel(c_short(axis_move), vel))
        print("my_SetPos", gts.GT_SetPos(c_short(axis_move), pos.value))
        print("my_Update", gts.GT_Update(1 << axis_move - 1))
        time.sleep(5)
        sts = c_long()
        clock = c_ulong()
        print("GT_GetSts():", gts.GT_GetSts(c_short(axis_move), byref(sts), c_short(1), byref(clock)))
        print(sts.value)
        if (sts.value == 576):
            print("GT_ClrSts():", gts.GT_ClrSts(c_short(axis_move), c_short(1)))
            time.sleep(5)
            print('GT_SetCaptureMode', gts.GT_SetCaptureMode(c_short(axis_move), c_short(1)))
            #            pos = c_long(int(80000000))
            #            vel = c_double(float(1))
            #            print("my_SetVel", gts.GT_SetVel(c_short(2), vel))
            #            print("my_SetPos", gts.GT_SetPos(c_short(2), pos.value))
            #            print("my_Update", gts.GT_Update(1 << 2 - 1))
            print("111")
            pos = c_long(int(80000000))
            vel = c_double(float(1))
            acc = c_double(float(0.25))
            dec = c_double(float(0.125))
            smooth = c_double(float(25))
            #            p2p = TTrapPrm()
            p2p.acc = acc
            p2p.dec = dec
            p2p.smoothTime = smooth
            p2p.velStart = 0
            print("1111")
            print("my_PrfJog", gts.GT_PrfTrap(c_short(axis_move)))
            print("my_SetTrapPrm", gts.GT_SetTrapPrm(c_short(axis_move), byref(p2p)))
            print("my_SetVel", gts.GT_SetVel(c_short(axis_move), vel))
            print("my_SetPos", gts.GT_SetPos(c_short(axis_move), pos.value))
            print("my_Update", gts.GT_Update(1 << axis_move - 1))
            print("GT_ClrSts():", gts.GT_ClrSts(c_short(axis_move), c_short(1)))
            print("GT_GetSts():", gts.GT_GetSts(c_short(axis_move), byref(sts), c_short(1), byref(clock)))
            print(sts.value)
            capture = c_short(int(0))
            position = c_long(int(0))
            clock = c_ulong()
            time.sleep(8)
            print("GT_ClrSts():", gts.GT_ClrSts(c_short(axis_move), c_short(1)))
            print('GT_GetCSts',
                  gts.GT_GetCaptureStatus(axis_move, byref(capture), byref(position), c_short(1), byref(clock)))
            print(capture.value)
            print(position.value)
            print('GT_Stop', gts.GT_Stop(c_long(0xff), c_long(0xff)))
            if (capture.value == 1):
                HomeCapture = position
                print(HomeCapture.value)
                print('GT_Stop', gts.GT_Stop(c_long(0xff), c_long(0xff)))
                time.sleep(2)
                vel = c_double(float(2))
                print("my_SetVel", gts.GT_SetVel(c_short(axis_move), vel))
                print("my_SetPos", gts.GT_SetPos(c_short(axis_move), HomeCapture))
                print("my_Update", gts.GT_Update(1 << axis_move - 1))
                #                position = c_double()
                #                clock = c_ulong()
                #                print("GT_GetPosition():", gts.GT_GetPrfPos(c_short(axis_move), byref(position),c_short(1),byref(clock)))
                #                print (position.value)
                #                self.editZ1.setText(str(position.value))

    def getPos(self, axis_move):
        position = c_double()
        clock = c_ulong()
        print("GT_GetPosition():", gts.GT_GetPrfPos(c_short(axis_move), byref(position), c_short(1), byref(clock)))
        return position.value

    def reset(self):
#        print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(0)))
#        self.homeback(axis_move=2)
#        time.sleep(3)
#        positionZ1 = self.getPos(axis_move=2)
#        print(positionZ1)
#        self.editZ1.setText(str(positionZ1))
#
#        print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(0)))
#        self.homeback(axis_move=4)
#        time.sleep(5)
#        positionY = self.getPos(axis_move=4)
#        print(positionY)
#        self.editY.setText(str(positionY))
#
#        print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(0)))
#        self.homeback(axis_move=5)
#        time.sleep(3)
#        positionZ = self.getPos(axis_move=5)
#        print(positionZ)
#        self.editZ.setText(str(positionZ))

        print("GT_SetCardNo_Card2():", gts.GT_SetCardNo(c_short(1)))
        self.homeback(axis_move=1)
        time.sleep(3)
        positionX3 = self.getPos(axis_move=1)
        print(positionX3)
        self.editZ.setText(str(positionX3))

        print("GT_SetCardNo_Card2():", gts.GT_SetCardNo(c_short(1)))
        self.homeback(axis_move=2)
        time.sleep(3)
        positionZ3 = self.getPos(axis_move=2)
        print(positionZ3)
        self.editZ.setText(str(positionZ3))

        print("GT_SetCardNo_Card2():", gts.GT_SetCardNo(c_short(1)))
        self.homeback(axis_move=3)
        time.sleep(3)
        positionA3 = self.getPos(axis_move=3)
        print(positionA3)
        self.editZ.setText(str(positionA3))

    #        position = c_double()
    #        clock = c_ulong()
    #        print("GT_GetPosition():", gts.GT_GetPrfPos(c_short(2), byref(position),c_short(1),byref(clock)))
    #        print (position.value)
    #        self.editZ1.setText(str(position.value))

    def getsts(self, axis_move):
        sts = c_long()
        clock = c_ulong()
        print("GT_GetSts():", gts.GT_GetSts(c_short(axis_move), byref(sts), c_short(1), byref(clock)))
        print(sts.value)

    def clrsts(self, axis_move):
        print("GT_ClrSts():", gts.GT_ClrSts(c_short(axis_move), c_short(1)))

    def move_getsts(self):
        axis_adjust = self.editAxis.text()
        if (axis_adjust == "Z1"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(0)))
            self.getsts(axis_move=2)
        elif (axis_adjust == "Y"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(0)))
            self.getsts(axis_move=4)
        elif (axis_adjust == "Z"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(0)))
            self.getsts(axis_move=5)
        elif (axis_adjust == "X3"):
            print("GT_SetCardNo_Card2():", gts.GT_SetCardNo(c_short(1)))
            self.getsts(axis_move=1)
        elif (axis_adjust == "Z3"):
            print("GT_SetCardNo_Card2():", gts.GT_SetCardNo(c_short(1)))
            self.getsts(axis_move=2)
        elif (axis_adjust == "A3"):
            print("GT_SetCardNo_Card2():", gts.GT_SetCardNo(c_short(1)))
            self.getsts(axis_move=3)
        else:
            print("please input the axis.")

    def move_clrsts(self):
        axis_adjust = self.editAxis.text()
        if (axis_adjust == "Z1"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(0)))
            self.clrsts(axis_move=2)
        elif (axis_adjust == "Y"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(0)))
            self.clrsts(axis_move=4)
        elif (axis_adjust == "Z"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(0)))
            self.clrsts(axis_move=5)
        elif (axis_adjust == "X3"):
            print("GT_SetCardNo_Card2():", gts.GT_SetCardNo(c_short(1)))
            self.clrsts(axis_move=1)
        elif (axis_adjust == "Z3"):
            print("GT_SetCardNo_Card2():", gts.GT_SetCardNo(c_short(1)))
            self.clrsts(axis_move=2)
        elif (axis_adjust == "A3"):
            print("GT_SetCardNo_Card2():", gts.GT_SetCardNo(c_short(1)))
            self.clrsts(axis_move=3)
        else:
            print("please input the axis.")

    def GenerateTestArray(self):
        # print(self.editZ.text())
        # print(float(self.editZ.text()))
        # positionZ = int(float(self.editZ.text()))
        # for i in range(10):
        #     self.testarray.append(int(positionZ + (i - 5) * 400))
        # print(self.testarray)

        print(self.editX3.text())
        print(float(self.editX3.text()))
        print(self.editZ3.text())
        print(float(self.editZ3.text()))
        print(self.editA3.text())
        print(float(self.editA3.text()))
        # positionX3 = int(float(self.editX3.text()))
        # positionZ3 = int(float(self.editZ3.text()))
        # positionA3 = int(float(self.editA3.text()))
        positionX3 = int(float(self.editX3.text()) * 200)
        positionZ3 = int(float(self.editZ3.text()) * 200)
        positionA3 = int(float(self.editA3.text()) * 200)
        brightness_light2 = int(self.Light2Chan3Edit.text())
        brightness_light1 = int(self.Light1Chan1Edit.text())
#        exposure_time = int(float(self.edit_exposure_time.text()))
        for i in range(10):
            array_temp = []
            array_temp.append(random.randint(positionX3 - 2000, positionX3 + 2000))
            array_temp.append(random.randint(positionZ3 - 2000, positionZ3 + 2000))
            array_temp.append(random.randint(positionA3 - 2000, positionA3 + 2000))
            array_temp.append(random.randint(brightness_light2 - 50, brightness_light2 + 50))
            array_temp.append(random.randint(brightness_light1 - 50, brightness_light1 + 50))
#            array_temp.append(random.randint(exposure_time - 2000, exposure_time + 2000))
            self.testarray.append(array_temp)
        self.testarray = np.array(self.testarray)
        print(self.testarray)
        
        print ("111111111111111111")
        time.sleep(2)
        self.AutoAcquireData()
        print ("222222222222222222")
        time.sleep(2)
        self.init_Population()
        print ("333333333333333333")
        time.sleep(2)
        self.Iterator()
        print ("444444444444444444")
        time.sleep(2)
        self.move_to_best()
        self.SaveTxt()

    def AutoAcquireData(self):
        #        for i in range (len(self.))
        start =time.time()
        file_name="QTGUI_Label_Test0/"
        self.AcquireImage(testarray=self.testarray,file_path_save=file_name)
        end =time.time()
        print (end-start)
    

    def AcquireImage(self, testarray,file_path_save):
        print (testarray)
        time.sleep(2)
        for i in range(len(testarray)):
            str_i = str(i)
            file_path_name = "QTGUI_Sample/" + "img_result" + str_i + ".jpg"
            print(file_path_name)
            # positionZ = testarray[i]
            # self.editZ.setText(str(positionZ))
            # self.gts_p2p(5, positionZ)
            # time.sleep(1)

            positionX3 = testarray[i][0]
            positionZ3 = testarray[i][1]
            positionA3 = testarray[i][2]
            brightness_light2 = testarray[i][3]
            brightness_light1 = testarray[i][4]
            brightness_light2_str=self.int2str(int(brightness_light2))
            brightness_light1_str=self.int2str(int(brightness_light1))
#            exposure_time = testarray[i][5]
            # self.editX3.setText(str(positionX3))
            # self.editZ3.setText(str(positionZ3))
            # self.editA3.setText(str(positionA3))
            self.editX3.setText('%.3f' % (positionX3 / 200))
            self.editZ3.setText('%.3f' % (positionZ3 / 200))
            self.editA3.setText('%.3f' % (positionA3 / 200))
            self.Light2Chan3Edit.setText(str(brightness_light2))
            self.Light1Chan1Edit.setText(str(brightness_light1))
#            self.Light1Chan2Edit.setText(str(brightness_light1))
#            self.Light1Chan3Edit.setText(str(brightness_light1))
#            self.Light1Chan4Edit.setText(str(brightness_light1))
#            self.edit_exposure_time.setText(str(exposure_time))
            self.move_to_destination(position_X3=positionX3, position_Z3=positionZ3, position_A3=positionA3)
            self.sendSerialLight2_V2(brightness_light2=brightness_light2_str)
            self.sendSerialLight1_V2(brightness_light1=brightness_light1_str)
            time.sleep(2)

#            mvccsdks = MvCamCtrlSDK()
#            mvccsdks.mv_cc_connect_device(condition='IP', condition_value='192.168.1.2')  # '10.67.131.120'
#            expousetime = round(float(self.edit_exposure_time.text()), 1)
#            expouseTime = c_float(expousetime)
#            mvccsdks.mv_cc_set_expousetime(expouseTime)
#            print("mv_cc_set_expousetime succeed")
            # 取流
#            print("mv_cc_start_grabbing_image")
#            self.mvccsdks.mv_cc_start_grabbing_image()  # MV_CC_StartGrabbing
            self.mvccsdks.mv_cc_set_trigger()
            print ("trigger successfully")
            image_frame = self.mvccsdks.mv_cc_get_one_frame_image()  # file_path='D:\\a.jpg'
#            image_frame = self.mvccsdks.mv_cc_get_one_frame_image()
            image = image_frame['RawImage']
            Width = image_frame['Width']
            Height = image_frame['Height']
            self.imgOri = np.reshape(image[:Height * Width], (Height, Width))
            
            cv.imwrite("QTGUI_Label_Test/process001.png", self.imgOri)
            self.imgLabel = copy.copy(self.imgOri[:, :])
    #        image_tmp = cv.imread('a.jpg', 0)
            image_tmp = cv.imread('QTGUI_Label_Test/process001.png', 0)
            img_resize = self.picture_resize(imgOri=image_tmp, Label=self.labelImg1)
    
            cv.imwrite("QTGUI_Label/process001_large.png", img_resize)  # img_resize
            qImgT_large = QtGui.QPixmap("QTGUI_Label/process001_large.png")
            self.labelImg1.setPixmap(qImgT_large)
            QtWidgets.QApplication.processEvents()
            
            for j in range(len(self.Array_ROI)):
                file_path_name2=file_path_save + "img_result" + "_region_"+str(j)+"_"+str_i + ".jpg"
                ROI_X = self.Array_ROI[j][0]
                ROI_X_1 = self.Array_ROI[j][1]
                ROI_Y = self.Array_ROI[j][2]
                ROI_Y_1 = self.Array_ROI[j][3]
                img_processed = copy.copy(self.imgOri[int(ROI_Y / self.ratio):int(ROI_Y_1 / self.ratio),
                                          int(ROI_X / self.ratio):int(ROI_X_1 / self.ratio)])
                cv.imwrite(file_path_name2, img_processed)
                self.Show_ROI(file_path_name2,ID=j)
                QtWidgets.QApplication.processEvents()

            #            image_tmp=cv.imread('a.jpg', 0)

            # 停流
#            mvccsdks.mv_cc_stop_grabbing_image()
#            print("mv_cc_stop_grabbing_image")
#            # 断开相机连接
#            mvccsdks.mv_cc_disconnect_device()

#    def sendSerialLight1(self):
#        print("准备发送")
#        if (self.ser1.isOpen()):
#            strLight1 = ("SpA0%s#SpB0%s#SpC0%s#SpD0%s#" % (
#                self.Light1Chan1Edit.text(), self.Light1Chan2Edit.text(), self.Light1Chan3Edit.text(),
#                self.Light1Chan4Edit.text()))
#            self.ser1.write(bytes(strLight1, encoding="utf8"))
#            print("发送成功", strLight1)
#        else:
#            print("发送失败")
#
#    def sendSerialLight2(self):
#        print("准备发送")
#        if (self.ser2.isOpen()):
#            strLight2 = ("SpA0%s#SpB0%s#SpC0%s#SpD0%s#" % (
#                self.Light2Chan1Edit.text(), self.Light2Chan2Edit.text(), self.Light2Chan3Edit.text(),
#                self.Light2Chan4Edit.text()))
#            self.ser2.write(bytes(strLight2, encoding="utf8"))
#            print("发送成功", strLight2)
#        else:
#            print("发送失败")
#
#    def sendSerialLight3(self):
#        print("准备发送")
#        if (self.ser3.isOpen()):
#            strLight3 = ("SpA0%s#SpB0%s#SpC0%s#SpD0%s#" % (
#                self.Light3Chan1Edit.text(), self.Light3Chan2Edit.text(), self.Light3Chan3Edit.text(),
#                self.Light3Chan4Edit.text()))
#            self.ser3.write(bytes(strLight3, encoding="utf8"))
#            print("发送成功", strLight3)
#        else:
#            print("发送失败")
#
#    def sendSerialLight4(self):
#        print("准备发送")
#        if (self.ser4.isOpen()):
#            strLight4 = ("SpA0%s#SpB0%s#SpC0%s#SpD0%s#" % (
#                self.Light4Chan1Edit.text(), self.Light4Chan2Edit.text(), self.Light4Chan3Edit.text(),
#                self.Light4Chan4Edit.text()))
#            self.ser4.write(bytes(strLight4, encoding="utf8"))
#            print("发送成功", strLight4)
#        else:
#            print("发送失败")
#
#    def sendSerialLight5(self):
#        print("准备发送")
#        if (self.ser5.isOpen()):
#            strLight5 = ("SpA0%s#SpB0%s#SpC0%s#SpD0%s#" % (
#                self.Light5Chan1Edit.text(), self.Light5Chan2Edit.text(), self.Light5Chan3Edit.text(),
#                self.Light5Chan4Edit.text()))
#            self.ser5.write(bytes(strLight5, encoding="utf8"))
#            print("发送成功", strLight5)
#        else:
#            print("发送失败")

    def picture_resize(self, imgOri, Label):
        height = imgOri.shape[0]
        width = imgOri.shape[1]
        if (height > width):
            ratioY = Label.height() / (height + 0.0)
            self.ratio = ratioY
            height2 = Label.height()
            width2 = int(width * ratioY + 0.5)
            imgPro = cv.resize(imgOri, (width2, height2))
        else:
            ratioX = Label.width() / (width + 0.0)
            self.ratio = ratioX
            width2 = Label.width()
            height2 = int(height * ratioX + 0.5)
            imgPro = cv.resize(imgOri, (width2, height2))
            #            imgPro=cv.resize(imgOri, (100, 100), interpolation=cv.INTER_CUBIC)
        return imgPro
    
    def picture_resize2(self, imgOri, Label):
        height = imgOri.shape[0]
        width = imgOri.shape[1]
        print (height)
        print (width)
        if (height > width):
            ratioY = Label.height() / (height + 0.0)
            height2 = Label.height()
            width2 = int(width * ratioY + 0.5)
            imgPro = cv.resize(imgOri, (width2, height2))
        else:
            ratioX = Label.width() / (width + 0.0)
            width2 = Label.width()
            height2 = int(height * ratioX + 0.5)
            imgPro = cv.resize(imgOri, (width2, height2))
            #            imgPro=cv.resize(imgOri, (100, 100), interpolation=cv.INTER_CUBIC)
        return imgPro

    def get_Camera_image(self):
#        mvccsdks = MvCamCtrlSDK()
#        # 连接设备
#        mvccsdks.mv_cc_connect_device(
#            condition='IP', condition_value='192.168.1.2')  # '10.67.131.120'
#
#        expousetime = round(float(self.edit_exposure_time.text()), 1)
#        expouseTime = c_float(expousetime)
#        mvccsdks.mv_cc_set_expousetime(expouseTime);
#        print("mv_cc_set_expousetime succeed")
#        # 取流
#        print("mv_cc_start_grabbing_image")
#        mvccsdks.mv_cc_start_grabbing_image()  # MV_CC_StartGrabbing
        
#        expousetime = round(float(self.edit_exposure_time.text()), 1)
#        expouseTime = c_float(expousetime)
#        self.mvccsdks.mv_cc_set_expousetime(expouseTime);
#        print("mv_cc_set_expousetime succeed")
        start=time.time()
        self.mvccsdks.mv_cc_set_trigger()
        print ("trigger successfully")
#        image_frame = self.mvccsdks.mv_cc_get_one_frame_image('a.jpg')  # file_path='D:\\a.jpg'
        image_frame = self.mvccsdks.mv_cc_get_one_frame_image()
        image = image_frame['RawImage']
        Width = image_frame['Width']
        Height = image_frame['Height']
        self.imgOri = np.reshape(image[:Height * Width], (Height, Width))
        cv.imwrite("QTGUI_Label_Test/process001.png", self.imgOri)
        self.imgLabel = copy.copy(self.imgOri[:, :])
#        image_tmp = cv.imread('a.jpg', 0)
        image_tmp = cv.imread('QTGUI_Label_Test/process001.png', 0)
        img_resize = self.picture_resize(imgOri=image_tmp, Label=self.labelImg1)

        cv.imwrite("QTGUI_Label/process001_large.png", img_resize)  # img_resize
        qImgT_large = QtGui.QPixmap("QTGUI_Label/process001_large.png")
        self.labelImg1.setPixmap(qImgT_large)
        end=time.time()
        print (end-start)

#        # 停流
#        mvccsdks.mv_cc_stop_grabbing_image()
#        print("mv_cc_stop_grabbing_image")
#        # 断开相机连接
#        mvccsdks.mv_cc_disconnect_device()

#    def fun_takephoto(self):
#        return 0
#
#    def Brenna_img(self, img_arr):
#        img_arr = img_arr
#        m = 0
#        w, h = img_arr.shape
#        for i in range(w):
#            for j in range(h - 2):
#                m = m + np.square(img_arr[i, j + 2] - img_arr[i, j])
#        return m
#
#    def Reblur_image(self, img1):
#        Gradient1 = self.Brenna_img(img1)
#        # Gradient2 = self.Brenna_img(img2)  # filter image
#        # Gradient3 = self.Brenna_img(img3)  # filter image
#
#        #        alpha = (Gradient2 - Gradient3) / (Gradient1 - Gradient2)
#        #        alpha = Gradient2 / Gradient1\
#        alpha = 1.0 / Gradient1
#        return alpha
#    def imconv1(self,image_array, suanzi):
#        image = image_array.copy()
#        dim1,dim2 = image.shape
#        for i in range(1,dim1-1):
#            for j in range(1,dim2-1):
#                image[i,j] = (image_array[(i-1):(i+2),(j-1):(j+2)]*suanzi).sum()
#        
#        image = image*(255.0/image.max())
#
#        return image 
#    def Fun_Target2(self,image_array):
#        suanzi_x = np.array([[-1, 0, 1],[-1, 0, 1], [-1, 0, 1]])
#        suanzi_y = np.array([[-1, -1, -1],[0, 0, 0], [1, 1, 1]])
#        image_x = self.imconv1(image_array,suanzi_x)
#        image_y = self.imconv1(image_array,suanzi_y)
#
#        
#        image_xy = np.sqrt(image_x**2+image_y**2)
#        
#        image_xy = (255.0/image_xy.max())*image_xy
#        image_xy=filters.gaussian(image_xy, 0.5)
#        image_xy = sm.opening(image_xy,sm.square(4))
#        image_xy = sm.closing(image_xy,sm.square(1))
#
#
#
#        boundary_sum =1.0/ np.sum(image_xy)
#        return boundary_sum

    def init_Population(self):
        #        class_path = "/home/huawei/DOE_DataSets/Logo-Victoria-0927-RAW/Victoria-AL00C-Lan/OK/H/"
        start=time.time()
        for i in range(len(self.testarray)):
            print(i)

            self.pbest[i] = self.testarray[i]
            # take photoes by using the parameters
            str_i = str(i)
            goal_sum=0
#            ROI_weigth = [1, 1, -1]
            for j in range(len(self.Array_ROI)):
                file_path = "QTGUI_Label_Test0/" + "img_result" + "_region_" + str(j) + "_" + str_i + ".jpg"
#                img = Image.open(file_path).convert('L')
#
#                img_arr = np.array(img)
            #            img_arr = img_arr1[y_up:y_down, x_up:x_down]
            #     img2 = img.filter(ImageFilter.GaussianBlur(radius=2))
            #     img3 = img2.filter(ImageFilter.GaussianBlur(radius=2))
            #     img2_arr = np.array(img2)
            #     img3_arr = np.array(img3)
            #
            #     tmp = self.Reblur_image(img_arr, img2_arr, img3_arr)
#                tmp = self.Reblur_image(img_arr)
                img=cv.imread(file_path)
                gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
                dest=cv.Sobel(gray,cv.CV_16U,1,1)
                mean_index=np.mean(dest)
                tmp=1/mean_index
#                tmp=mean_index
                goal_sum += self.ROI_weigth[j] * tmp

            self.p_fit[i] = goal_sum
            if (goal_sum < self.fit):
                self.fit = goal_sum
                self.gbest = self.testarray[i]
        print("successfully:", self.gbest)
        print(self.fit)
        time.sleep(2)
        end=time.time()
        print (end-start)

    def Iterator(self):
        #        x_up = coord[0][0]
        #        y_up = coord[0][1]
        #        x_down = coord[1][0]
        #        y_down = coord[1][1]
        start=time.time()
#        ROI_weigth = [1,1,1]
        for t in range(self.max_iter):
            print("tttttttttttt=", t)
            # slow down the time
            #            class_path = "/home/huawei/DOE_DataSets/Logo-Victoria-0927-RAW/Victoria-AL00C-Lan/OK/H/"
            for i in range(self.pN):
                # take photoes by using X[i]


                str_i = str(i)
                goal_sum = 0
                for j in range(len(self.Array_ROI)):
                    file_path = "QTGUI_Label_Test"+str(t)+"/" + "img_result" + "_region_" + str(j) + "_" + str_i + ".jpg"
#                    img = Image.open(file_path).convert('L')
#
#                    img_arr = np.array(img)
#                    #            img_arr = img_arr1[y_up:y_down, x_up:x_down]
#                    #     img2 = img.filter(ImageFilter.GaussianBlur(radius=2))
#                    #     img3 = img2.filter(ImageFilter.GaussianBlur(radius=2))
#                    #     img2_arr = np.array(img2)
#                    #     img3_arr = np.array(img3)
#                    #
#                    #     tmp = self.Reblur_image(img_arr, img2_arr, img3_arr)
#                    tmp = self.Reblur_image(img_arr)
                    img=cv.imread(file_path)
                    gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
                    dest=cv.Sobel(gray,cv.CV_16U,1,1)
                    mean_index=np.mean(dest)
                    tmp=1/mean_index
#                    tmp=mean_index
                    goal_sum += self.ROI_weigth[j]*tmp

                #                temp = self.function(self.X[i])
                if (goal_sum < self.p_fit[i]):
                    self.p_fit[i] = goal_sum
                    self.pbest[i] = self.testarray[i]

                    if (self.p_fit[i] < self.fit):
                        self.gbest = self.testarray[i]
                        self.fit = self.p_fit[i]
            self.target_loss.append(self.fit)
            array_show=np.array(self.target_loss)
            dr = Figure_Canvas()
            dr.show_curve(y_value=array_show)
            graphicscene = QtWidgets.QGraphicsScene()
            graphicscene.addWidget(dr)
            self.graphicview.setScene(graphicscene)
            self.graphicview.show()
            for i in range(self.pN):
                self.V[i] = self.w * self.V[i] + self.c1 * self.r1 * (
                    self.pbest[i] - self.testarray[i]) + self.c2 * self.r2 * (self.gbest - self.testarray[i])
                self.testarray[i] = self.testarray[i] + self.V[i]

            print(self.testarray)
            file_path_save_name="QTGUI_Label_Test"+str(t+1)+"/"
            self.AcquireImage(testarray=self.testarray,file_path_save=file_path_save_name)
        print(self.gbest)
        end=time.time()
        print (end-start)
#    def Iterator2(self):
#        for t in range(self.max_iter2):
#            print("tttttttttttt=", t)
#            # slow down the time
#            #            class_path = "/home/huawei/DOE_DataSets/Logo-Victoria-0927-RAW/Victoria-AL00C-Lan/OK/H/"
#            for i in range(self.pN):
#                # take photoes by using X[i]
#
#
#                str_i = str(i)
#                goal_sum = 0
#                for j in range(len(self.Array_ROI)):
#                    file_path = "QTGUI_Label_Test/" + "img_result" + "_region_" + str(j) + "_" + str_i + ".jpg"
#                    img = Image.open(file_path).convert('L')
#                    image = sm.opening(img,sm.square(13))
#                    image_array=filters.gaussian(image, 1.0)
#                    #            img_arr = img_arr1[y_up:y_down, x_up:x_down]
#                    #     img2 = img.filter(ImageFilter.GaussianBlur(radius=2))
#                    #     img3 = img2.filter(ImageFilter.GaussianBlur(radius=2))
#                    #     img2_arr = np.array(img2)
#                    #     img3_arr = np.array(img3)
#                    #
#                    #     tmp = self.Reblur_image(img_arr, img2_arr, img3_arr)
#                    tmp = self.Fun_Target2(image_array)
#                    goal_sum += tmp
#
#                #                temp = self.function(self.X[i])
#                if (goal_sum < self.p_fit[i]):
#                    self.p_fit[i] = goal_sum
#                    self.pbest[i] = self.testarray[i]
#
#                    if (self.p_fit[i] < self.fit):
#                        self.gbest = self.testarray[i]
#                        self.fit = self.p_fit[i]
#            self.target_array.append(self.fit)
#
#            for i in range(self.pN):
#                self.V[i] = self.w * self.V[i] + self.c1 * self.r1 * (
#                    self.pbest[i] - self.testarray[i]) + self.c2 * self.r2 * (self.gbest - self.testarray[i])
#                self.testarray[i] = self.testarray[i] + self.V[i]
#
#            print(self.testarray)
#            self.AcquireImage(testarray=self.testarray)
#        print(self.gbest)

    def move_to_best(self):
        positionX3 = self.gbest[0]
        positionZ3 = self.gbest[1]
        positionA3 = self.gbest[2]
        brightness_light2 = self.gbest[3]
        brightness_light1 = self.gbest[4]
#        exposure_time = self.gbest[5]
        self.editX3.setText(str(positionX3))
        self.editZ3.setText(str(positionZ3))
        self.editA3.setText(str(positionA3))
        self.editX3.setText('%.3f' % (positionX3 / 200))
        self.editZ3.setText('%.3f' % (positionZ3 / 200))
        self.editA3.setText('%.3f' % (positionA3 / 200))
        self.Light2Chan3Edit.setText(str(brightness_light2))
        self.Light1Chan1Edit.setText(str(brightness_light1))
#        self.Light1Chan2Edit.setText(str(brightness_light1))
#        self.Light1Chan3Edit.setText(str(brightness_light1))
#        self.Light1Chan4Edit.setText(str(brightness_light1))
#        self.edit_exposure_time.setText(str(exposure_time))

        self.move_to_destination(position_X3=positionX3, position_Z3=positionZ3, position_A3=positionA3)
        self.sendSerialLight2_V2(brightness_light2=brightness_light2)
        self.sendSerialLight1_V2(brightness_light1=brightness_light1)
        time.sleep(2)

#        mvccsdks = MvCamCtrlSDK()
#        mvccsdks.mv_cc_connect_device(condition='IP', condition_value='192.168.1.2')  # '10.67.131.120'
#        expousetime = round(float(self.edit_exposure_time.text()), 1)
#        expouseTime = c_float(expousetime)
#        mvccsdks.mv_cc_set_expousetime(expouseTime);
#        print("mv_cc_set_expousetime succeed")
#        # 取流
#        print("mv_cc_start_grabbing_image")
#        mvccsdks.mv_cc_start_grabbing_image()  # MV_CC_StartGrabbing
        self.mvccsdks.mv_cc_set_trigger()
        print ("trigger successfully")
        image_frame = self.mvccsdks.mv_cc_get_one_frame_image()  # file_path='D:\\a.jpg'

        image = image_frame['RawImage']
        Width = image_frame['Width']
        Height = image_frame['Height']
        self.imgOri = np.reshape(image[:Height * Width], (Height, Width))
        cv.imwrite("QTGUI_Label_Test/BestPhoto.jpg", self.imgOri)
        for j in range(len(self.Array_ROI)):
            file_path_name2 = "QTGUI_Label_Test/" + "_bestPhoto" + "_region_" + str(j) + ".jpg"
            ROI_X = self.Array_ROI[j][0]
            ROI_X_1 = self.Array_ROI[j][1]
            ROI_Y = self.Array_ROI[j][2]
            ROI_Y_1 = self.Array_ROI[j][3]
            img_processed = copy.copy(self.imgOri[int(ROI_Y / self.ratio):int(ROI_Y_1 / self.ratio),
                                      int(ROI_X / self.ratio):int(ROI_X_1 / self.ratio)])
            cv.imwrite(file_path_name2, img_processed)
            self.Show_ROI(file_path_name2,ID=j)
            QtWidgets.QApplication.processEvents()
        # print(self.ROI_X)
        # print(self.ROI_Y)
        # self.img_processed = copy.copy(self.imgOri[int(self.ROI_Y / self.ratio):int(self.ROI_Y_1 / self.ratio),
        #                                int(self.ROI_X / self.ratio):int(self.ROI_X_1 / self.ratio)])
        # cv.imwrite("Best_Photo1.jpg", self.imgOri)
        # cv.imwrite("Best_Photo2.jpg", self.img_processed)

        #            shutil.rmtree(class_path)
        #            os.mkdir(class_path)
        # choose the camera and take photoes by using the parameters X and producing images in path class_path

    def sendSerialLight1_V2(self, brightness_light1):
        print("准备发送")
        if (self.ser1.isOpen()):
            strLight1 = ("SpA0%s#SpB0%s#SpC0%s#SpD0%s#" % (
                brightness_light1, '000', '000', '000'))
            self.ser1.write(bytes(strLight1, encoding="utf8"))
            print("发送成功", strLight1)
        else:
            print("发送失败")

    def sendSerialLight2_V2(self, brightness_light2):
        print("准备发送")
        if (self.ser2.isOpen()):
            strLight1 = ("SpA0%s#SpB0%s#SpC0%s#SpD0%s#" % (
                '000', '000', brightness_light2, '000'))
            self.ser2.write(bytes(strLight1, encoding="utf8"))
            print("发送成功", strLight1)
        else:
            print("发送失败")
            
#    def sendSerialLight2_V2(self, brightness_light2):
#        print("准备发送")
#        if (self.ser2.isOpen()):
#            strLight1 = ("SpA0%s#SpB0%s#SpC0%s#SpD0%s#" % (
#                brightness_light2, brightness_light2, brightness_light2, '000'))
#            self.ser2.write(bytes(strLight1, encoding="utf8"))
#            print("发送成功", strLight1)
#        else:
#            print("发送失败")l

    def SendWL(self):
        position_Y = 21400
        print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(0)))
        self.gts_p2p(4, position_Y)
#        self.editY.setText(str(position_Y))
        

    def ReturnWL(self):
        position_Y = 0
        print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(0)))
        self.gts_p2p(4, position_Y)
#        self.editY.setText(str(position_Y))
        

    def SetLight(self):
#        brightness_light2 = int(self.Light2Chan3Edit.text())
#        brightness_light1 = int(self.Light1Chan1Edit.text())
        brightness_light2 = int(self.Light2Chan3Edit.text())
        brightness_light1 = int(self.Light1Chan1Edit.text())
        brightness_light2_str=self.int2str(brightness_light2)
        brightness_light1_str=self.int2str(brightness_light1)
        print (brightness_light2_str)
        print (brightness_light1_str)
        self.sendSerialLight2_V2(brightness_light2=brightness_light2_str)
        self.sendSerialLight1_V2(brightness_light1=brightness_light1_str)

    def AddROI(self):
        current_ROI = [self.ROI_X, self.ROI_X_1, self.ROI_Y, self.ROI_Y_1]
        self.Array_ROI.append(current_ROI)
        cv.rectangle(self.imgLabel, (int(self.ROI_X / self.ratio), int(self.ROI_Y / self.ratio)),
                     (int(self.ROI_X_1 / self.ratio), int(self.ROI_Y_1 / self.ratio)), (0, 0, 255), 5)
        cv.imwrite("QTGUI_Label_Test/process002.png", self.imgLabel)

    def PrintROI(self):
        print("The number of ROI:%d" % len(self.Array_ROI))
        print(self.Array_ROI)
        for i in range(len(self.Array_ROI)):
            file_path = "QTGUI_Label_Test/ROI_process00" + str(i) + ".png"
            ROI_X = self.Array_ROI[i][0]
            ROI_X_1 = self.Array_ROI[i][1]
            ROI_Y = self.Array_ROI[i][2]
            ROI_Y_1 = self.Array_ROI[i][3]
            img_processed = copy.copy(self.imgOri[int(ROI_Y / self.ratio):int(ROI_Y_1 / self.ratio),
                                      int(ROI_X / self.ratio):int(ROI_X_1 / self.ratio)])
            cv.imwrite(file_path, img_processed)
            self.Show_ROI(file_path,ID=i)
            QtWidgets.QApplication.processEvents()
            
    def Show_ROI(self,path,ID):
        if ID==0:
            image_tmp = cv.imread(path, 0)
            img_resize = self.picture_resize2(imgOri=image_tmp, Label=self.labelImg2)
    
            cv.imwrite("QTGUI_Label/process002_large.png", img_resize)  # img_resize
            qImgT_large = QtGui.QPixmap("QTGUI_Label/process002_large.png")
            self.labelImg2.setPixmap(qImgT_large)
        elif ID==1:
            image_tmp = cv.imread(path, 0)
            img_resize = self.picture_resize2(imgOri=image_tmp, Label=self.labelImg3)
    
            cv.imwrite("QTGUI_Label/process003_large.png", img_resize)  # img_resize
            qImgT_large = QtGui.QPixmap("QTGUI_Label/process003_large.png")
            self.labelImg3.setPixmap(qImgT_large)
        else:
            image_tmp = cv.imread(path, 0)
            img_resize = self.picture_resize2(imgOri=image_tmp, Label=self.labelImg4)
    
            cv.imwrite("QTGUI_Label/process004_large.png", img_resize)  # img_resize
            qImgT_large = QtGui.QPixmap("QTGUI_Label/process004_large.png")
            self.labelImg4.setPixmap(qImgT_large)
            
            
            
            
#    def Linkcamera(self):
#        self.mvccsdks = MvCamCtrlSDK()
#        # 连接设备
#        camera_ID=int (self.bg1.checkedId())
#        print (camera_ID)
#        print (type(camera_ID))
#        if camera_ID==1:
#            self.mvccsdks.mv_cc_connect_device(
#                condition='IP', condition_value='192.168.1.2')  # '10.67.131.120'
#        elif camera_ID==2:
#            self.mvccsdks.mv_cc_connect_device(
#                condition='IP', condition_value='192.168.2.2')
#        else:
#            self.mvccsdks.mv_cc_connect_device(
#                condition='IP', condition_value='192.168.3.2')
#        expousetime = round(float(self.edit_exposure_time.text()), 1)
#        expouseTime = c_float(expousetime)
#        self.mvccsdks.mv_cc_set_expousetime(expouseTime);
#        print("mv_cc_set_expousetime succeed")
#        # 取流
#        print("mv_cc_start_grabbing_image")
#        self.mvccsdks.mv_cc_start_grabbing_image()  # MV_CC_StartGrabbing
     
    def Linkcamera(self):
#        self.mvccsdks = MvCamCtrlSDK()
#        # 连接设备
#        self.mvccsdks.mv_cc_connect_device(
#                condition='IP', condition_value='192.168.2.2')
#        expousetime = round(float(self.edit_exposure_time.text()), 1)
#        expouseTime = c_float(expousetime)
#        self.mvccsdks.mv_cc_set_expousetime(expouseTime);
#        print("mv_cc_set_expousetime succeed")
#        # 取流
#        print("mv_cc_start_grabbing_image")
#        self.mvccsdks.mv_cc_start_grabbing_image()  # MV_CC_StartGrabbing
        self.mvccsdks = MvCamCtrlSDK()
        # 连接设备



        self.mvccsdks.mv_cc_connect_device(condition='IP', condition_value='192.168.2.2')

        expousetime = round(float(self.edit_exposure_time.text()), 1)
        expouseTime = c_float(expousetime)
        self.mvccsdks.mv_cc_set_expousetime(expouseTime);
        print("mv_cc_set_expousetime succeed")
        # 取流
        triggermode=1
        self.mvccsdks.mv_cc_set_triggermode(triggerMode=triggermode)
        print("mv_cc_set_triggermode succeed")
        print("mv_cc_start_grabbing_image")
        self.mvccsdks.mv_cc_start_grabbing_image()  # MV_CC_StartGrabbing
    
    def UnLinkcamera(self):
        triggermode=0
        self.mvccsdks.mv_cc_set_triggermode(triggerMode=triggermode)
        print("mv_cc_set_triggermode succeed")
        self.mvccsdks.mv_cc_stop_grabbing_image()
        print("mv_cc_stop_grabbing_image")
        # 断开相机连接
        self.mvccsdks.mv_cc_disconnect_device()
        
    def SaveTxt(self):
#        print (self.target_array)
#        np.savetxt('text1228.txt',self.target_array)
        
        print (self.target_loss)
        np.savetxt('iter_data.txt',self.target_loss)
#        print (self.bg1.checkedId())
        
    def int2str(self,input):
        if (input>255):
            output='255'
        elif (input>99):
            output=str(input)
        elif (input>9):
            output='0'+str(input)
        elif (input>0):
            output='00'+str(input)
        else:
            output='000'
        return output
    def Load_Logo(self):
        file_path="Logo2.png"
        self.Logo=cv.imread(file_path)
        print (self.Logo.shape)
        img1=self.picture_resize(imgOri=self.Logo,Label=self.labelImg5)
        cv.imwrite("Logo_resize.png",img1)
        qImgT1=QtGui.QPixmap("Logo_resize.png")
        self.labelImg5.setPixmap(qImgT1)
        
    def fun_combox(self):
        print (self.comboxproduct.currentIndex())
        index=self.comboxproduct.currentIndex()
        if index ==0:
            self.ROI_weigth=[1,1,1]
            self.Light1Chan1Edit.setText("80")
            self.Light2Chan3Edit.setText("150")
        elif index==1:
            self.ROI_weigth=[1,1,1]
            self.Light1Chan1Edit.setText("150")
            self.Light2Chan3Edit.setText("150")
        else:
            self.ROI_weigth=[1,1,-1]
            self.Light1Chan1Edit.setText("150")
            self.Light2Chan3Edit.setText("150")
            
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    motion_control = Motion_Control()
    motion_control.show()
    sys.exit(app.exec_())




