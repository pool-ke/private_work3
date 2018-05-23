# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 10:40:43 2018

@author: kWX491567
"""


import numpy as np
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QRadioButton,QButtonGroup
import os
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



class Motion_Control(QtWidgets.QWidget):
    def closeEvent(self, a0: QtGui.QCloseEvent):
        reply = QtWidgets.QMessageBox.question(self,
                                               '本程序',
                                               "是否要退出程序？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            if self.cameraOn==1:
                self.UnLinkcamera()
                self.cameraOn=0
            QtGui.QCloseEvent.accept()
        else:
            QtGui.QCloseEvent.ignore()
    def __init__(self):
        super(Motion_Control, self).__init__()
        self.setGeometry(30, 30, 780, 650)
        self.setWindowTitle("Logo机台光源轴参数控制系统")

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
        self.cameraOn=0

        self.mvccsdks=None

    def initUI(self):
        self.btnGetCamera = QtWidgets.QPushButton(u"触发拍照", self)
        self.btnGetCamera.move(600, 370)
        self.btnGetCamera.resize(80,50)
        self.btnGetCamera.clicked.connect(self.get_Camera_image)
        self.labelImg1 = QtWidgets.QLabel(self)
        self.labelImg1.setAlignment(Qt.AlignTop)  # self.labelImg1.setAlignment(Qt.AlignCenter)  # AlignTop
        pe = QPalette()
        self.labelImg1.setAutoFillBackground(True)
        pe.setColor(QPalette.Window, Qt.gray)
        self.labelImg1.setPalette(pe)
        self.labelImg1.move(30, 30)
        self.labelImg1.resize(550, 400)
        

        self.labelX3 = QtWidgets.QLabel(u"水平X3:", self)
        self.editX3 = QtWidgets.QLineEdit(self)

        self.labelA3 = QtWidgets.QLabel(u"旋转A3:", self)
        self.editA3 = QtWidgets.QLineEdit(self)

        self.labelZ3 = QtWidgets.QLabel(u"垂直Z3:", self)
        self.editZ3 = QtWidgets.QLineEdit(self)

        self.labelX1 = QtWidgets.QLabel(u"水平X1:", self)
        self.editX1 = QtWidgets.QLineEdit(self)

        self.labelA1 = QtWidgets.QLabel(u"旋转A1:", self)
        self.editA1 = QtWidgets.QLineEdit(self)

        self.labelZ1 = QtWidgets.QLabel(u"垂直Z1:", self)
        self.editZ1 = QtWidgets.QLineEdit(self)

        self.labelH = QtWidgets.QLabel(u"面光高度Z:", self)
        self.editH = QtWidgets.QLineEdit(self)
        
        self.labeltext2 = QtWidgets.QLabel("控制轴号：",self)


#         self.label_exposure_time = QtWidgets.QLabel(u"曝光度:", self)
# #        self.label_exposure_time.move(180, 140)
#         self.edit_exposure_time = QtWidgets.QLineEdit(self)
#         self.edit_exposure_time.setText("4000.0")

        self.buttonMove = QtWidgets.QPushButton("参数设置", self)
        # self.buttonMove.move(600,80)
        self.buttonMove.clicked.connect(self.fun_move)


        self.editAxis = QtWidgets.QLineEdit(self)
        self.editAxis.resize(50, 20)
        self.editAxis.setText("X3")

        self.buttonLink = QtWidgets.QPushButton("启动设备", self)
        self.buttonLink.move(600, 20)
        self.buttonLink.resize(80,50)
        self.buttonLink.clicked.connect(self.connect_link)

        self.buttonUnLink = QtWidgets.QPushButton(u"关闭设备", self)
        self.buttonUnLink.move(600, 80)
        self.buttonUnLink.resize(80, 50)
        self.buttonUnLink.clicked.connect(self.connect_unlink)

        self.buttonMoveUp = QtWidgets.QPushButton(u"前进", self)
#        self.buttonMoveUp.move(450, 80)
        self.buttonMoveUp.pressed.connect(self.move_up)
        self.buttonMoveUp.released.connect(self.move_stop)

        self.buttonMoveDown = QtWidgets.QPushButton(u"后退", self)
#        self.buttonMoveUp.move(450, 110)
        self.buttonMoveDown.pressed.connect(self.move_down)
        self.buttonMoveDown.released.connect(self.move_stop)

        self.buttonReset = QtWidgets.QPushButton(u"复位", self)
#        self.buttonReset.move(450, 140)
        self.buttonReset.clicked.connect(self.reset)

        self.buttonGetsts = QtWidgets.QPushButton(u"获取状态", self)
#        self.buttonGetsts.move(450, 170)
        self.buttonGetsts.clicked.connect(self.move_getsts)

        self.buttonclrsts = QtWidgets.QPushButton(u"清除限位", self)
#        self.buttonclrsts.move(450, 200)
        self.buttonclrsts.clicked.connect(self.move_clrsts)



        self.buttonSendWL = QtWidgets.QPushButton(u"拍照位", self)
#        self.buttonSendWL.move(450, 380)
        self.buttonSendWL.clicked.connect(self.SendWL)

        self.buttonReturnWL = QtWidgets.QPushButton(u"物料位", self)
#        self.buttonReturnWL.move(450, 410)
        self.buttonReturnWL.clicked.connect(self.ReturnWL)

        self.buttonSetLigiht = QtWidgets.QPushButton(u"设置光照", self)
        # self.buttonSetLigiht.move(600, 110)
        self.buttonSetLigiht.clicked.connect(self.SetLight)
        
        self.buttonLinkCam = QtWidgets.QPushButton(u"连接相机", self)
        self.buttonLinkCam.clicked.connect(self.Linkcamera)
        
        self.buttonUnLinkCam = QtWidgets.QPushButton(u"断开相机", self)
        self.buttonUnLinkCam.clicked.connect(self.UnLinkcamera)

        self.expousetime_set = QtWidgets.QPushButton(u"曝光设置", self)
        self.expousetime_set.clicked.connect(self.Expousetime_Set)
        
#        self.buttonIter2 = QtWidgets.QPushButton(u"Iterator2", self)
#        self.buttonIter2.move(450, 590)
#        self.buttonIter2.clicked.connect(self.Iterator2)
        
#        self.buttonSave = QtWidgets.QPushButton(u"SaveTxt", self)
#        self.buttonSave.move(450, 620)
#        self.buttonSave.clicked.connect(self.SaveTxt)
        
        self.rb11 = QRadioButton('相机一',self)
        self.rb12 = QRadioButton('相机二',self)
        self.rb12.setChecked(1)
        self.rb13 = QRadioButton('相机三', self)
        
        self.bg1 = QButtonGroup(self)
        self.bg1.addButton(self.rb11,1)
        self.bg1.addButton(self.rb12,2)
        self.bg1.addButton(self.rb13,3)

        self.label_exposure_time1 = QtWidgets.QLabel(u"曝光度:", self)
        self.label_exposure_time2 = QtWidgets.QLabel(u"曝光度:", self)
        self.label_exposure_time3 = QtWidgets.QLabel(u"曝光度:", self)

        self.edit_exposure_time1 = QtWidgets.QLineEdit(self)
        self.edit_exposure_time1.setText("4000.0")
        self.edit_exposure_time2 = QtWidgets.QLineEdit(self)
        self.edit_exposure_time2.setText("4000.0")
        self.edit_exposure_time3 = QtWidgets.QLineEdit(self)
        self.edit_exposure_time3.setText("4000.0")
        
        self.radioWidget = QtWidgets.QTabWidget(self)
        self.radioWidget.move(30, 450)
        self.radioWidget.resize(240, 180)
        
        CameraWidget = QtWidgets.QWidget(self.radioWidget)
        CameraLayout = QtWidgets.QGridLayout()
        CameraLayout.addWidget(self.rb11, 0, 0)
        CameraLayout.addWidget(self.rb12, 1, 0)
        CameraLayout.addWidget(self.rb13, 2, 0)
        CameraLayout.addWidget(self.label_exposure_time1, 0, 1)
        CameraLayout.addWidget(self.label_exposure_time2, 1, 1)
        CameraLayout.addWidget(self.label_exposure_time3, 2, 1)
        CameraLayout.addWidget(self.edit_exposure_time1, 0, 2)
        CameraLayout.addWidget(self.edit_exposure_time2, 1, 2)
        CameraLayout.addWidget(self.edit_exposure_time3, 2, 2)
        CameraLayout.addWidget(self.buttonLinkCam,3,0)
        CameraLayout.addWidget(self.buttonUnLinkCam,3,1)
        CameraLayout.addWidget(self.expousetime_set, 3, 2)
        self.radioWidget.setLayout(CameraLayout)
        self.radioWidget.addTab(CameraWidget, "相机选择")

        
        self.axisWidget=QtWidgets.QTabWidget(self)
        self.axisWidget.move(600,140)
        self.axisWidget.resize(150,220)
        
        
        
        AxisWidget=QtWidgets.QWidget(self.axisWidget)
        AxisLayout=QtWidgets.QGridLayout()
        AxisLayout.addWidget(self.labeltext2,0,0)
        AxisLayout.addWidget(self.editAxis,0,1)
        AxisLayout.addWidget(self.buttonMoveUp,1,0)
        AxisLayout.addWidget(self.buttonMoveDown,2,0)
        AxisLayout.addWidget(self.buttonReset,3,0)
        AxisLayout.addWidget(self.buttonGetsts,1,1)
        AxisLayout.addWidget(self.buttonclrsts,2,1)
        AxisLayout.addWidget(self.buttonSendWL,4,0)
        AxisLayout.addWidget(self.buttonReturnWL,4,1)
        self.axisWidget.setLayout(AxisLayout)
        self.axisWidget.addTab(AxisWidget,"单轴控制")
        
        self.paraWidget=QtWidgets.QTabWidget(self)
        self.paraWidget.move(300,450)
        self.paraWidget.resize(450,180)
        
        Light1Chan1 = QtWidgets.QLabel("面光源")
        self.Light1Chan1Edit = QtWidgets.QLineEdit()
        Light2Chan3 = QtWidgets.QLabel("左光源：")
        self.Light2Chan3Edit = QtWidgets.QLineEdit()

        Light3Chan3 = QtWidgets.QLabel("右光源：")
        self.Light3Chan3Edit = QtWidgets.QLineEdit()
        
        
        ParaWidget=QtWidgets.QWidget(self.paraWidget)
        ParaLayout=QtWidgets.QGridLayout()
        ParaLayout.addWidget(Light2Chan3,0,0)
        ParaLayout.addWidget(self.Light2Chan3Edit,0,1)
        ParaLayout.addWidget(self.labelX3,1,0)
        ParaLayout.addWidget(self.editX3,1,1)
        ParaLayout.addWidget(self.labelZ3,2,0)
        ParaLayout.addWidget(self.editZ3,2,1)
        ParaLayout.addWidget(self.labelA3,3,0)
        ParaLayout.addWidget(self.editA3,3,1)
        ParaLayout.addWidget(Light3Chan3, 0, 2)
        ParaLayout.addWidget(self.Light3Chan3Edit, 0, 3)
        ParaLayout.addWidget(self.labelX1, 1, 2)
        ParaLayout.addWidget(self.editX1, 1, 3)
        ParaLayout.addWidget(self.labelZ1, 2, 2)
        ParaLayout.addWidget(self.editZ1, 2, 3)
        ParaLayout.addWidget(self.labelA1, 3, 2)
        ParaLayout.addWidget(self.editA1, 3, 3)
        ParaLayout.addWidget(Light1Chan1, 0, 4)
        ParaLayout.addWidget(self.Light1Chan1Edit, 0, 5)
        ParaLayout.addWidget(self.labelH, 1, 4)
        ParaLayout.addWidget(self.editH, 1, 5)
        ParaLayout.addWidget(self.buttonMove, 2, 4)
        ParaLayout.addWidget(self.buttonSetLigiht, 3, 4)
        self.paraWidget.setLayout(ParaLayout)
        self.paraWidget.addTab(ParaWidget,"参数设置")
        
        self.editX3.setText("33")
        self.editZ3.setText("0")
        self.editA3.setText("-55")
        self.editX1.setText("33")
        self.editZ1.setText("0")
        self.editA1.setText("-55")
        self.editH.setText("0")
        self.Light1Chan1Edit.setText("80")
        self.Light2Chan3Edit.setText("150")
        self.Light3Chan3Edit.setText("150")

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
#        self.labeltext.setText("GT_Open")

    def connect_unlink(self):
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
#        self.labeltext.setText("GT_Close")

    def fun_move(self):
        position_X3 = float(self.editX3.text())
        position_Z3 = float(self.editZ3.text())
        position_A3 = float(self.editA3.text())

        position_X1 = float(self.editX1.text())
        position_Z1 = float(self.editZ1.text())
        position_A1 = float(self.editA1.text())

        print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(1)))
        self.gts_p2p(4, position_X1 * 200)
        self.gts_p2p(5, position_Z1 * 200)
        self.gts_p2p(6, position_A1 * 200)

        print("GT_SetCardNo_Card2():", gts.GT_SetCardNo(c_short(1)))
        self.gts_p2p(1, position_X3 * 200)
        self.gts_p2p(2, position_Z3 * 200)
        self.gts_p2p(3, position_A3 * 200)
        self.SetLight()
        
        if(self.cameraOn==1):
            
            time.sleep(1)
            self.get_Camera_image()



#    def move_to_destination(self, position_X3, position_Z3, position_A3):
#        print("GT_SetCardNo_Card2():", gts.GT_SetCardNo(c_short(1)))
#        self.gts_p2p(1, position_X3)
#        self.gts_p2p(2, position_Z3)
#        self.gts_p2p(3, position_A3)
#        print("GT_ClrSts():", gts.GT_ClrSts(c_short(1), c_short(1)))
#        print("GT_ClrSts():", gts.GT_ClrSts(c_short(2), c_short(1)))
#        print("GT_ClrSts():", gts.GT_ClrSts(c_short(3), c_short(1)))
#
#        print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(0)))
#        self.gts_p2p(1, position_X3)
#        self.gts_p2p(2, position_Z3)
#        self.gts_p2p(3, position_A3)
#        print("GT_ClrSts():", gts.GT_ClrSts(c_short(1), c_short(1)))
#        print("GT_ClrSts():", gts.GT_ClrSts(c_short(2), c_short(1)))
#        print("GT_ClrSts():", gts.GT_ClrSts(c_short(3), c_short(1)))

    def move_up(self):
        axis_adjust = self.editAxis.text()
        position = c_double()
        clock = c_ulong()
        if (axis_adjust == "X1"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(1)))
            self.gts_jog(4, -1)
        elif(axis_adjust == "Z1"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(1)))
            self.gts_jog(5, -1)
        elif (axis_adjust == "A1"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(1)))
            self.gts_jog(6, -1)
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
        if (axis_adjust == "X1"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(1)))
            print('GT_Stop', gts.GT_Stop(c_long(0xff), c_long(0xff)))
            position = c_double()
            clock = c_ulong()
            print("GT_GetPosition():", gts.GT_GetPrfPos(c_short(4), byref(position), c_short(1), byref(clock)))
            position_X1 = position.value / 2000
            self.editZ1.setText('%.3f' % position_X1)
            # self.editZ1.setText(str(position.value/2000))
        elif (axis_adjust == "Z1"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(1)))
            print('GT_Stop', gts.GT_Stop(c_long(0xff), c_long(0xff)))
            position = c_double()
            clock = c_ulong()
            print("GT_GetPosition():", gts.GT_GetPrfPos(c_short(5), byref(position), c_short(1), byref(clock)))
            position_Z1 = position.value / 2000
            self.editZ1.setText('%.3f' % position_Z1)
        elif (axis_adjust == "A1"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(1)))
            print('GT_Stop', gts.GT_Stop(c_long(0xff), c_long(0xff)))
            position = c_double()
            clock = c_ulong()
            print("GT_GetPosition():", gts.GT_GetPrfPos(c_short(6), byref(position), c_short(1), byref(clock)))
            position_A1 = position.value / 2000
            self.editA1.setText('%.3f' % position_A1)
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
            self.editH.setText('%.3f' % position_Z)
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
        if (axis_adjust == "X1"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(1)))
            self.gts_jog(4, 1)
        elif (axis_adjust == "Z1"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(1)))
            self.gts_jog(5, 1)
        elif (axis_adjust == "A1"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(1)))
            self.gts_jog(6, 1)
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


        print("GT_SetCardNo_Card2():", gts.GT_SetCardNo(c_short(1)))
        self.homeback(axis_move=6)
        time.sleep(3)
        positionX3 = self.getPos(axis_move=1)
        print(positionX3)
        self.editZ.setText(str(positionX3))

        print("GT_SetCardNo_Card2():", gts.GT_SetCardNo(c_short(1)))
        self.homeback(axis_move=7)
        time.sleep(3)
        positionZ3 = self.getPos(axis_move=2)
        print(positionZ3)
        self.editZ.setText(str(positionZ3))

        print("GT_SetCardNo_Card2():", gts.GT_SetCardNo(c_short(1)))
        self.homeback(axis_move=8)
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
        if (axis_adjust == "X1"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(1)))
            self.getsts(axis_move=4)
        elif (axis_adjust == "Z1"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(1)))
            self.getsts(axis_move=5)
        elif (axis_adjust == "A1"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(1)))
            self.getsts(axis_move=6)
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
        if (axis_adjust == "X1"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(1)))
            self.clrsts(axis_move=4)
        elif (axis_adjust == "Z1"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(1)))
            self.clrsts(axis_move=5)
        elif (axis_adjust == "A1"):
            print("GT_SetCardNo_Card1():", gts.GT_SetCardNo(c_short(1)))
            self.clrsts(axis_move=6)
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
    

    def get_Camera_image(self):
#        start=time.time()
#        self.mvccsdks.mv_cc_set_trigger()
#        print ("trigger successfully")
        image_frame = self.mvccsdks.mv_cc_get_one_frame_image('a.bmp')
        image_tmp = cv.imread('a.bmp', 0)
        img_resize = self.picture_resize(imgOri=image_tmp, Label=self.labelImg1)

        cv.imwrite("QTGUI_Label/process001_large.png", img_resize)  # img_resize
        qImgT_large = QtGui.QPixmap("QTGUI_Label/process001_large.png")
        self.labelImg1.setPixmap(qImgT_large)


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
        brightness_light3 = int(self.Light3Chan3Edit.text())
        brightness_light2 = int(self.Light2Chan3Edit.text())
        brightness_light1 = int(self.Light1Chan1Edit.text())
        brightness_light3_str = self.int2str(brightness_light3)
        brightness_light2_str=self.int2str(brightness_light2)
        brightness_light1_str=self.int2str(brightness_light1)
        print (brightness_light3_str)
        print (brightness_light2_str)
        print (brightness_light1_str)
        self.sendSerialLight3_V2(brightness_light3=brightness_light3_str)
        self.sendSerialLight2_V2(brightness_light2=brightness_light2_str)
        self.sendSerialLight1_V2(brightness_light1=brightness_light1_str)
        
        
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

    def sendSerialLight3_V2(self, brightness_light3):
        print("准备发送")
        if (self.ser3.isOpen()):
            strLight1 = ("SpA0%s#SpB0%s#SpC0%s#SpD0%s#" % (
                '000', '000', '000', brightness_light3))
            self.ser3.write(bytes(strLight1, encoding="utf8"))
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
#            print("发送失败")
            
            
            
            
    def Linkcamera(self):
        self.mvccsdks = MvCamCtrlSDK()
        # 连接设备
        camera_ID=int (self.bg1.checkedId())
        print (camera_ID)
        print (type(camera_ID))
        if camera_ID==1:
            self.mvccsdks.mv_cc_connect_device(
                condition='IP', condition_value='192.168.1.2')  # '10.67.131.120'
            expousetime = round(float(self.edit_exposure_time1.text()), 1)
            expouseTime = c_float(expousetime)
            self.mvccsdks.mv_cc_set_expousetime(expouseTime)
            print("mv_cc_set_expousetime succeed")
        elif camera_ID==2:
            self.mvccsdks.mv_cc_connect_device(
                condition='IP', condition_value='192.168.2.2')
            expousetime = round(float(self.edit_exposure_time2.text()), 1)
            expouseTime = c_float(expousetime)
            self.mvccsdks.mv_cc_set_expousetime(expouseTime)
            print("mv_cc_set_expousetime succeed")
        else:
            self.mvccsdks.mv_cc_connect_device(
                condition='IP', condition_value='192.168.3.2')
            expousetime = round(float(self.edit_exposure_time3.text()), 1)
            expouseTime = c_float(expousetime)
            self.mvccsdks.mv_cc_set_expousetime(expouseTime)
            print("mv_cc_set_expousetime succeed")
        # expousetime = round(float(self.edit_exposure_time.text()), 1)
        # expouseTime = c_float(expousetime)
        # self.mvccsdks.mv_cc_set_expousetime(expouseTime);
        # print("mv_cc_set_expousetime succeed")
        # 取流
        self.cameraOn=1
#        triggermode=1
#        self.mvccsdks.mv_cc_set_triggermode(triggerMode=triggermode)
#        print("mv_cc_set_triggermode succeed")
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
        self.cameraOn=0

    def Expousetime_Set(self):
        self.UnLinkcamera();
        self.Linkcamera();
        print("parameter of camera set succeed");
        
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
            
            
            
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    motion_control = Motion_Control()
    motion_control.show()
    sys.exit(app.exec_())


