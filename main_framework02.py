import numpy as np
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QPalette,QFont
from PyQt5.QtWidgets import QMessageBox
import os
import json
import math
import copy
import sys
import ctypes
from ctypes import *
import time
import cv2 as cv
# import serial
# import serial.tools.list_ports
# from MvCamCtrlSDK import MvCamCtrlSDK
from PIL import ImageFilter
from PIL import Image
from pylab import *
import copy
import random

class VIDI_Show(QtWidgets.QWidget):
    def __init__(self):
        super(VIDI_Show, self).__init__()
        self.setGeometry(30, 30, 1300, 930)
        self.setWindowTitle("深度学习图像检测系统")

        self.initUI()
        self.Load_Picture()
        self.Load_Logo()

    def initUI(self):
        self.labelImg1 = QtWidgets.QLabel(self)
        self.labelImg1.setAlignment(Qt.AlignTop)  # self.labelImg1.setAlignment(Qt.AlignCenter)  # AlignTop
        pe = QPalette()
        self.labelImg1.setAutoFillBackground(True)
        pe.setColor(QPalette.Window, Qt.gray)
        self.labelImg1.setPalette(pe)
        self.labelImg1.move(50, 50)
        self.labelImg1.resize(500, 400)

        self.labelImg2 = QtWidgets.QLabel(self)
        self.labelImg2.setAlignment(Qt.AlignTop)  # self.labelImg1.setAlignment(Qt.AlignCenter)  # AlignTop
        pe = QPalette()
        self.labelImg2.setAutoFillBackground(True)
        pe.setColor(QPalette.Window, Qt.gray)
        self.labelImg2.setPalette(pe)
        self.labelImg2.move(600, 50)
        self.labelImg2.resize(500, 400)

        self.labelImg3 = QtWidgets.QLabel(self)
        self.labelImg3.setAlignment(Qt.AlignTop)  # self.labelImg1.setAlignment(Qt.AlignCenter)  # AlignTop
        pe = QPalette()
        self.labelImg3.setAutoFillBackground(True)
        pe.setColor(QPalette.Window, Qt.gray)
        self.labelImg3.setPalette(pe)
        self.labelImg3.move(50,500)
        self.labelImg3.resize(500, 400)

        self.labelImg4 = QtWidgets.QLabel(self)
        self.labelImg4.setAlignment(Qt.AlignTop)  # self.labelImg1.setAlignment(Qt.AlignCenter)  # AlignTop
        pe = QPalette()
        self.labelImg4.setAutoFillBackground(True)
        pe.setColor(QPalette.Window, Qt.gray)
        self.labelImg4.setPalette(pe)
        self.labelImg4.move(600, 500)
        self.labelImg4.resize(500, 400)

        self.labelImg5 = QtWidgets.QLabel(self)
        self.labelImg5.move(1150, 110)
        self.labelImg5.resize(97, 282)

        self.labeltext1 = QtWidgets.QLabel("钻雕蓝手机Logo（Part1）：", self)
        self.labeltext1.move(50, 20)
        self.labeltext1.setFont(QFont("Roman times",20,QFont.Bold))


        self.labeltext2 = QtWidgets.QLabel("钻雕蓝手机Logo（Part2）:", self)
        self.labeltext2.move(600, 20)
        self.labeltext2.setFont(QFont("Roman times",20,QFont.Bold))

        self.labeltext3 = QtWidgets.QLabel("光器件：", self)
        self.labeltext3.move(50, 470)
        self.labeltext3.setFont(QFont("Roman times",20,QFont.Bold))

        self.labeltext4 = QtWidgets.QLabel("耀石黑手机Logo：", self)
        self.labeltext4.move(600, 470)
        self.labeltext4.setFont(QFont("Roman times",20,QFont.Bold))

        self.filechoose=QtWidgets.QListWidget(self)
        self.filechoose.move(1150,500)
        self.filechoose.resize(100,300)

        self.filechoose.itemClicked.connect(self.itemClick)

        self.labeltext5 = QtWidgets.QLabel("图片选择", self)
        self.labeltext5.move(1150, 780)

        self.labeltext6 = QtWidgets.QLabel( self)
        self.labeltext6.move(450, 20)
        self.labeltext6.resize(30,20)

        self.labeltext7 = QtWidgets.QLabel(self)
        self.labeltext7.move(1000, 20)
        self.labeltext7.resize(30, 20)

        self.labeltext8 = QtWidgets.QLabel(self)
        self.labeltext8.move(450, 470)
        self.labeltext8.resize(30, 20)

        self.labeltext9 = QtWidgets.QLabel(self)
        self.labeltext9.move(1000, 470)
        self.labeltext9.resize(30, 20)

        # self.btnLoadPicture = QtWidgets.QPushButton("加载图片", self)
        # self.btnLoadPicture.move(1200, 50)
        # self.btnLoadPicture.clicked.connect(self.Load_Picture)



        self.btnDetection = QtWidgets.QPushButton("检测", self)
        self.btnDetection.move(1150,830)
        self.btnDetection.clicked.connect(self.Detection_Picture)
        
#        self.StatuInfo = QtWidgets.QLabel(self)
#        self.StatuInfo.move(50, 902)
#        self.StatuInfo.resize(150, 20)
#        self.StatuInfo.setText('准备就绪')
        
        self.labelStatuInfo = QtWidgets.QLabel(self)
        self.labelStatuInfo.move(1150, 50)
        self.labelStatuInfo.resize(100, 20)

        self.labelStatuInfo.setText('准备检测！')
        self.labelStatuInfo.setFont(QFont("Roman times",15,QFont.Bold))
        pe = QPalette()
        pe.setColor(QPalette.WindowText,Qt.green)
        self.labelStatuInfo.setPalette(pe)


    def itemClick(self):
        main_path1="Display\ZuanLan_0926-Part1\RawImages"
        main_path5="Display\ZuanLan_0926-Part1\Results"
        file_path1 =main_path1+"/"+self.filechoose.currentItem().text()
        file_path5 =main_path5+"/"+self.filechoose.currentItem().text()
        self.imgOri1=cv.imread(file_path1)
        img1=self.picture_resize(imgOri=self.imgOri1,Label=self.labelImg1)
        cv.imwrite("QTGUI/process001.png",img1)
        self.imgOri5=cv.imread(file_path5)
        img5=self.picture_resize(imgOri=self.imgOri5,Label=self.labelImg1)
        cv.imwrite("QTGUI/process005.png",img5)
        qImgT1=QtGui.QPixmap("QTGUI/process001.png")
        self.labelImg1.setPixmap(qImgT1)

        main_path2 = "Display\ZuanLan_0926\RawImages"
        main_path6 = "Display\ZuanLan_0926\Results"
        file_path2 = main_path2 + "/" + self.filechoose.currentItem().text()
        file_path6 = main_path6 + "/" + self.filechoose.currentItem().text()
        self.imgOri2 = cv.imread(file_path2)
        img2 = self.picture_resize(imgOri=self.imgOri2, Label=self.labelImg2)
        cv.imwrite("QTGUI/process002.png", img2)
        self.imgOri6=cv.imread(file_path6)
        img6=self.picture_resize(imgOri=self.imgOri6,Label=self.labelImg2)
        cv.imwrite("QTGUI/process006.png",img6)
        qImgT2 = QtGui.QPixmap("QTGUI/process002.png")
        self.labelImg2.setPixmap(qImgT2)

        main_path3 = "Display\AOI\RawImages"
        main_path7 = "Display\AOI\Results"
        file_path3 = main_path3 + "/" + self.filechoose.currentItem().text()
        file_path7 = main_path7 + "/" + self.filechoose.currentItem().text()
        self.imgOri3 = cv.imread(file_path3)
        img3 = self.picture_resize(imgOri=self.imgOri3, Label=self.labelImg3)
        cv.imwrite("QTGUI/process003.png", img3)
        self.imgOri7=cv.imread(file_path7)
        img7=self.picture_resize(imgOri=self.imgOri7,Label=self.labelImg3)
        cv.imwrite("QTGUI/process007.png",img7)
        qImgT3 = QtGui.QPixmap("QTGUI/process003.png")
        self.labelImg3.setPixmap(qImgT3)
#
        main_path4 = "Display\Hei_1130\RawImages"
        main_path8 = "Display\Hei_1130\Results"
        file_path4 = main_path4 + '/' + self.filechoose.currentItem().text()
        file_path8 = main_path8 + "/" + self.filechoose.currentItem().text()
        self.imgOri4 = cv.imread(file_path4)
        img4 = self.picture_resize(imgOri=self.imgOri4, Label=self.labelImg4)
        cv.imwrite("QTGUI/process004.png", img4)
        self.imgOri8=cv.imread(file_path8)
        img8=self.picture_resize(imgOri=self.imgOri8,Label=self.labelImg4)
        cv.imwrite("QTGUI/process008.png",img8)
        qImgT4 = QtGui.QPixmap("QTGUI/process004.png")
        self.labelImg4.setPixmap(qImgT4)
        
        self.labeltext6.setText('')
        self.labeltext7.setText('')
        self.labeltext8.setText('')
        self.labeltext9.setText('')
        
        self.labelStatuInfo.setText('准备检测！')
        self.labelStatuInfo.setFont(QFont("Roman times",15,QFont.Bold))
        pe = QPalette()
        pe.setColor(QPalette.WindowText,Qt.green)
        self.labelStatuInfo.setPalette(pe)

    def Load_Picture(self):
        file_path ="Display\AOI\RawImages"
        print (file_path)
        if os.path.isdir(file_path):
            allImgs=os.listdir(file_path)
            for imgTemp in allImgs:
                self.filechoose.addItem(imgTemp)
                
    def Load_Logo(self):
        file_path="444.png"
        self.Logo=cv.imread(file_path)
        img1=self.picture_resize(imgOri=self.Logo,Label=self.labelImg5)
        cv.imwrite("QTGUI/process100.png",img1)
        qImgT1=QtGui.QPixmap("QTGUI/process100.png")
        self.labelImg5.setPixmap(qImgT1)
        return 0
        
    def Detection_Picture(self):
#        self.StatuInfo.setText('正在检测中，请稍后！')
        self.labelStatuInfo.setText('检测进行中，请稍后')
        self.labelStatuInfo.setFont(QFont("Roman times",15,QFont.Bold))
        pe = QPalette()
        pe.setColor(QPalette.WindowText,Qt.green)
        self.labelStatuInfo.setPalette(pe)
        
        time.sleep(2)
        
        qImgT1 = QtGui.QPixmap("QTGUI/process005.png")
        self.labelImg1.setPixmap(qImgT1)
        
        qImgT2 = QtGui.QPixmap("QTGUI/process006.png")
        self.labelImg2.setPixmap(qImgT2)
        
        qImgT3 = QtGui.QPixmap("QTGUI/process007.png")
        self.labelImg3.setPixmap(qImgT3)
        
        qImgT4 = QtGui.QPixmap("QTGUI/process008.png")
        self.labelImg4.setPixmap(qImgT4)

#         result=([["NG","NG","NG","OK"],
#                  ["OK","OK","OK","NG"],
#                  ["OK","NG","OK","OK"],
#                  ["NG","NG","NG","OK"],
#                  ["NG","OK","NG","NG"],
#                  ["OK","OK","OK","OK"]])
    
        result={'Picture001.jpg':["NG","NG","NG","OK"],
                 'Picture002.jpg':["OK","OK","OK","NG"],
                 'Picture003.jpg':["OK","NG","OK","OK"],
                 'Picture004.jpg':["NG","NG","NG","OK"],
                 'Picture005.jpg':["NG","OK","NG","NG"],
                 'Picture006.jpg':["OK","OK","OK","OK"]}
        color={"OK":Qt.green,"NG":Qt.red}
    
        Index=self.filechoose.currentItem().text()
#         print (Index)
#         print (result[Index])
        pe=QPalette()
        self.labeltext6.setText(result[Index][0])
        self.labeltext6.setFont(QFont("Roman times",20,QFont.Bold))
        pe.setColor(QPalette.WindowText,color[result[Index][0]])
        self.labeltext6.setPalette(pe)
        self.labeltext7.setText(result[Index][1])
        self.labeltext7.setFont(QFont("Roman times",20,QFont.Bold))
        pe.setColor(QPalette.WindowText,color[result[Index][1]])
        self.labeltext7.setPalette(pe)
        self.labeltext8.setText(result[Index][2])
        self.labeltext8.setFont(QFont("Roman times",20,QFont.Bold))
        pe.setColor(QPalette.WindowText,color[result[Index][2]])
        self.labeltext8.setPalette(pe)
        self.labeltext9.setText(result[Index][3])
        self.labeltext9.setFont(QFont("Roman times",20,QFont.Bold))
        pe.setColor(QPalette.WindowText,color[result[Index][3]])
        self.labeltext9.setPalette(pe)
        
        self.labelStatuInfo.setText('检测完成！')
        self.labelStatuInfo.setFont(QFont("Roman times",15,QFont.Bold))
        pe = QPalette()
        pe.setColor(QPalette.WindowText,Qt.red)
        self.labelStatuInfo.setPalette(pe)
#        self.StatuInfo.setText('检测完成！')

    def picture_resize(self, imgOri, Label):
        height = imgOri.shape[0]
        width = imgOri.shape[1]
        print (Label.height())
        print (Label.width())
        print (height)
        print (width)
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
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    motion_control = VIDI_Show()
    motion_control.show()
    sys.exit(app.exec_())