#-*-coding:utf-8-*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from GetName import Ui_dialog
from communication import GetNamesByOption, Get_FieldAndItems, Get_AllTables, GetImageByName2, \
    DeleteTarFile, GetImageByName3, GetSizeByName
import os
import sys
import json
import copy
import threading
import pickle

class GetList(QDialog, Ui_dialog):
    export_finish_signal = pyqtSignal()
    show_progress_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(GetList, self).__init__(parent)
        self.setupUi(self)
        self.initUI()
        self.ConditionDist = {}
        self.headers = {
        'User - Agent': 'Mozilla / 5.0(Windows NT 6.1;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 70.0.3538.110Safari / 537.36',
        'Connection': 'close'
        }
        self.proxies = {
            'http': None, 'https': None
        }
        self.Enquiry_list = []
        self.IpAddress = "10.101.170.80:50007"
        self.item_list = []


    def get_all_tabel(self):
        #http get table list
        self.TabelSelecetComboBox.clear()
        for t in self.AllTabel:
            self.TabelSelecetComboBox.addItem(t)

    def initUI(self):

        self.QueryPushButton.clicked.connect(self.Enquiry)
        self.FeatureComboBox.activated[str].connect(self.showItemCommobox)
        self.TabelSelecetComboBox.activated[str].connect(self.GetTabel)
        self.AddConditionPushButton.clicked.connect(self.AddCondition)
        self.ConnectButton.clicked.connect(self.connect)
        self.ExportpushButton.clicked.connect(self.export)
        self.ExportprogressBar.setValue(0)
        self.ExportprogressBar.setVisible(True)
        self.ExportAccessTag = False
        self.ExportAccess()
        self.EnquiryAccessTag = False
        self.EnquiryAccess()
        self.export_finish_signal.connect(self.Export_finish)
        self.show_progress_signal.connect(self.Show_progressBar)
        self.ClearConditionPushButton.clicked.connect(self.ClearCondition)
        self.EnddateEdit.setDate(QDate.currentDate())


    def ExportAccess(self):
        self.ExportpushButton.setEnabled(self.ExportAccessTag)

    def EnquiryAccess(self):
        self.AddConditionPushButton.setEnabled(self.EnquiryAccessTag)
        self.TabelSelecetComboBox.setEnabled(self.EnquiryAccessTag)
        self.FeatureComboBox.setEnabled(self.EnquiryAccessTag)
        self.QueryPushButton.setEnabled(self.EnquiryAccessTag)
        self.ItemComboBox.setEnabled(self.EnquiryAccessTag)

    def connect(self):
        #connect the server and get the table list
        self.AllTabel = ["Table_1", "Table_2"]  # http get table list
        self.IpAddress = self.IPAddresstextEdit.toPlainText()
        QUERY_URL = "http://" + self.IpAddress + "/table_query"
        self.AllTabel = Get_AllTables(QUERY_URL,header=self.headers,proxy=self.proxies)
        if (type(self.AllTabel) != int):
            print (self.AllTabel)
            ConnectSuccessful = True
        else:
            print (u"连接服务器失败")
            ConnectSuccessful = False

        if ConnectSuccessful:
            self.get_all_tabel()
            self.GetTabel()
            self.EnquiryAccessTag = True
            self.EnquiryAccess()
        else:
            QMessageBox.warning(self, "Error", "链接失败", QMessageBox.Yes | QMessageBox.Yes)

    def check_time(self, end_time, begin_time):
        if end_time[3] > begin_time[3]:
            return True
        elif  end_time[3] == begin_time[3]:
            if end_time[0] > begin_time[0]:
                return True
            elif end_time[0] == begin_time[0]:
                if end_time[1] > begin_time[1]:
                    return True
                elif end_time[1] == begin_time[1]:
                    if end_time[2] >= begin_time[2]:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

    def time_format_change(self, begin_time, end_time):
        if len(begin_time[0]) == 1:
            begin_time[0] = "0" + begin_time[0]
        if len(begin_time[1]) == 1:
            begin_time[1] = "0" + begin_time[1]

        if len(end_time[0]) == 1:
            end_time[0] = "0" + end_time[0]
        if len(end_time[1]) == 1:
            end_time[1] = "0" + end_time[1]

        begin_time = begin_time[-1] + begin_time[0] + begin_time[1]
        end_time = end_time[-1] + end_time[0] + end_time[1]

        return begin_time, end_time

    def AddCondition(self):
        #update enquiry condition
        self.SQLtextEdit.clear()
        SQL = ""
        feature = self.FeatureComboBox.currentText()
        item = self.ItemComboBox.currentText()
        self.item_list = self.ConditionDist[feature]
        if item not in self.item_list:
            self.item_list.append(item)
        else:
            pass
        feature_list = list(self.ConditionDist.keys())
        if feature not in feature_list:
            self.ConditionDist.update({feature: self.item_list})
        else:
            self.ConditionDist[feature] = self.item_list
        print(self.ConditionDist)

        QueryCondition = str(self.ConditionDist)
        QueryCondition = QueryCondition.replace("],", "],\r")
        QueryCondition = QueryCondition.replace("{", " ")
        QueryCondition = QueryCondition.replace("}", "")
        self.SQLtextEdit.setText(QueryCondition)

    def ClearCondition(self):
        feature = self.FeatureComboBox.currentText()
        self.ConditionDist[feature] = []
        QueryCondition = str(self.ConditionDist)
        QueryCondition = QueryCondition.replace("],", "],\r")
        QueryCondition = QueryCondition.replace("{", " ")
        QueryCondition = QueryCondition.replace("}", "")
        self.SQLtextEdit.setText(QueryCondition)


    def showItemCommobox(self):
        self.ItemComboBox.clear()
        f = self.FeatureComboBox.currentText()
        self.item_list = self.item_dict[f]
        for item in self.item_list:
            self.ItemComboBox.addItem(item)

    def showFeatureCommobox(self):
        self.FeatureComboBox.clear()
        for f in self.feature_list:
            self.FeatureComboBox.addItem(f)
        self.showItemCommobox()

    def GetTabel(self):
        #获取http表内容
        self.Tabel = self.TabelSelecetComboBox.currentText()
        feature_list, item_dict = self.GetFeatureAndItem()
        if feature_list == 0 and item_dict == 0:
            return 0
        else:
            self.feature_list = feature_list
            self.item_dict = item_dict
            self.showFeatureCommobox()
            self.ConditionDist = {}
            #init enquiry condition
            for f in self.feature_list:
                self.ConditionDist.update({f: []})
            #update enquiry condition
            QueryCondition = str(self.ConditionDist)
            QueryCondition = QueryCondition.replace("],", "],\r")
            QueryCondition = QueryCondition.replace("{", " ")
            QueryCondition = QueryCondition.replace("}", "")
            #show enquiry condition
            self.SQLtextEdit.setText(QueryCondition)

    def GetFeatureAndItem(self):
        #http get table item and values
        table_name=self.Tabel
        QUERY_URL="http://" + self.IpAddress + "/table_field_query"
        FieldAndItems=Get_FieldAndItems(QUERY_URL,header=self.headers,proxy=self.proxies,table=table_name)
        if type(FieldAndItems) == int:
            QMessageBox.warning(self, "Error", "表信息获取失败", QMessageBox.Yes | QMessageBox.Yes)
            return 0, 0
        else:
            feature_list = list(FieldAndItems.keys())
        return feature_list, FieldAndItems

    def Enquiry(self):
        #reset the export information
        self.unsuccussful_export_image = []
        self.successful_export_number = 0
        self.ExportprogressBar.setValue(0)
        exportInfo = ""
        self.ExportResulttextEdit.setText(exportInfo)
        #get time
        end_time = self.EnddateEdit.dateTime().toString()#get time
        begin_time  = self.BegindateEdit.dateTime().toString()
        week = "周一 周二 周三 周四 周五 周六 周日".split(" ")
        month = "一 二 三 四 五 六 七 八 九 十".split(" ")
        month_num = [str(x + 1) for x in range(9)] + ["1"]
        for w in week:
            end_time = end_time.replace(w, "").lstrip()
            begin_time = begin_time.replace(w, "").lstrip()
        for i in range(10):
            end_time = end_time.replace(month[i], month_num[i]).lstrip()
            begin_time = begin_time.replace(month[i], month_num[i]).lstrip()
        end_time = end_time.replace("月", "").lstrip()
        begin_time = begin_time.replace("月", "").lstrip()
        end_time = end_time.split(" ")
        begin_time = begin_time.split(" ")
        Time_Check_flage = self.check_time(end_time, begin_time)
        begin_time, end_time = self.time_format_change(begin_time, end_time)
        #time checking
        if Time_Check_flage:
            enquiry_time = (begin_time, end_time)
        else:
            QMessageBox.warning(self, "Error", "日期输入错误", QMessageBox.Yes | QMessageBox.Yes)
            return 0
        #add time information into enquiry dict
        enquiry_Dict = copy.deepcopy(self.ConditionDist)
        for (k, v) in enquiry_Dict.items():
            if len(v) == 0:
                v.append("ALL")
        print(enquiry_Dict)

        feature_list = list(enquiry_Dict.keys())
        if "Time" not in feature_list:
            enquiry_Dict.update({"time_point": enquiry_time})
        else:
            enquiry_Dict["time_point"] = enquiry_time
        #get enquiry result
        self.Enquiry_list = self.getResult(enquiry_Dict)
        #enquiry result check
        if (type(self.Enquiry_list) == int) or (len(self.Enquiry_list) == 0):
            QMessageBox.warning(self, "Error", "未找到相应文件", QMessageBox.Yes | QMessageBox.Yes)
            self.ExportAccessTag = False
            self.ExportAccess()
        else:
            self.ExportAccessTag = True
            self.ExportAccess()
            # enquiry information update
            EnquiryResultInfo = "查询到图像数量：" + str(len(self.Enquiry_list))
            self.EnquiryResulttextEdit.setText(EnquiryResultInfo)
            self.ImagelistWidget.clear()
            self.ImagelistWidget.addItems(self.Enquiry_list)

    def getResult(self, enquiry_Dict):
        #return enquiry result
        option = {}
        option['table_name'] = self.TabelSelecetComboBox.currentText()
        option["field_option"] = json.dumps(enquiry_Dict)
        print(option)
        POST_URL1 = "http://" + self.IpAddress + "/image_query_by_option"
        Enquiry_list = GetNamesByOption(POST_URL1, option)
        return Enquiry_list

    def ExportThreading_by_name(self, Enquiry_list, ExportPath):
        #get image by file name
        POST_URL2 = "http://" + self.IpAddress + "/find_image_by_name"
        for img_name in Enquiry_list:
            self.status = GetImageByName2(POST_URL2, img_name, ExportPath)
            print(ExportPath)
            if self.status:
                self.unsuccussful_export_image.append(img_name)
            else:
                self.successful_export_number += 1
        self.exportInfo["导出文件数量"] = self.successful_export_number
        self.export_finish_signal.emit()

    def Split_list(self, Enquiry_list):
        #split image list by the number of posted images.
        temp_list = []
        split_list = []
        for i in range(len(Enquiry_list)):
            if i % 100 == 0 and len(temp_list) > 0:
                split_list.append(temp_list)
                temp_list = []
            temp_list.append(Enquiry_list[i])
        if len(temp_list) > 0:
            split_list.append(temp_list)
        return split_list

    def Split_list_by_size(self, Enquiry_list):
        #split image list by the size of posted images
        size_dict = self.Get_Image_size(Enquiry_list)
        sort_dict = sorted(size_dict.items(), key=lambda item: item[1], reverse=False)
        temp_list = []
        split_list = []
        current_size = 0
        self.total_size = 0 #total image list size
        self.zip_size_list = [] #each zip size
        for x in sort_dict:
            if current_size > 50:#the posted zip size is limited smaller than 100M
                split_list.append(temp_list)
                self.zip_size_list.append(current_size)
                temp_list = []
                current_size = 0
            current_size += x[1]/(1024*1024)
            self.total_size += x[1]/(1024*1024)
            temp_list.append(x[0])
        if len(temp_list) > 0:
            self.zip_size_list.append(current_size)
            split_list.append(temp_list)
        return split_list

    def ExportThreading_by_zip(self, Enquiry_list, ExportPath):
        #get image by zip
        POST_URL2 = "http://" + self.IpAddress + "/get_image_by_name2"
        #split image list
        split_list = self.Split_list_by_size(Enquiry_list)
        #reset export information
        self.unsuccussful_export_image = []
        self.successful_export_number = 0
        self.successful_export_size = 0
        #get image
        store_path = os.path.join(ExportPath, "result.pkl")
        for i, imlist in enumerate(split_list):
            data = {}
            data['image_names'] = json.dumps(imlist)
            self.status = GetImageByName3(POST_URL2, data, store_path)
            if self.status:
                self.unsuccussful_export_image.extend(imlist)
            else:
                self.successful_export_number += len(imlist)
                self.successful_export_size += self.zip_size_list[i]
                self.Image_loads(store_path)
            self.show_progress_signal.emit() #update the progress bar
        #update export information
        self.exportInfo["导出文件数量"] = self.successful_export_number
        self.export_finish_signal.emit()
        #request the server delete zip
        QUERY_URL = "http://" + self.IpAddress + "/delete_tarfile"
        status = DeleteTarFile(QUERY_URL, header=self.headers, proxy=self.proxies)
        os.remove(store_path)

    def Get_Image_size(self, Enquiry_list):
        #return the size dict of image {image_name:image_size,...}
        POST_URL4 = "http://" + self.IpAddress + "/get_size_by_name"
        data_name = {}
        data_name['image_names'] = json.dumps(Enquiry_list)
        size_dict = GetSizeByName(POST_URL4, data_name)
        return size_dict

    def Image_loads(self, pkl_path) :
        images_buffer_dict = pickle.loads(open(pkl_path, 'rb').read())
        for (imageId, imageBuffer) in images_buffer_dict.items():
            image_name = os.path.join(self.ExportPath, imageId)
            with open(image_name, 'wb') as f:
                f.write(imageBuffer)

    def Show_progressBar(self):
        # update the progress bar
        p = int(100 * (self.successful_export_size + 0.1) / (self.total_size + 0.1))
        self.ExportprogressBar.setValue(p)

    def Export_finish(self):
        QMessageBox.warning(self, "Successful", "导出完成", QMessageBox.Yes | QMessageBox.Yes)
        exportInfo = str(self.exportInfo) + "\n" + "导出失败文件:\n" + str(self.unsuccussful_export_image)
        self.ExportResulttextEdit.setText(exportInfo)

    def export(self):
        #export image
        self.exportInfo = {"导出路径": "", "导出文件数量":0}
        #get export path
        self.ExportPath = self.ExportPathSelection()
        #start export
        if self.ExportPath == "":
            self.exportInfo["导出文件数量"] = 0
        else:
            Export_thread = threading.Thread(target=self.ExportThreading_by_zip, args=(self.Enquiry_list, self.ExportPath))
            Export_thread.setDaemon(True)
            Export_thread.start()

    def ExportPathSelection(self):
        ExportPath = QFileDialog.getExistingDirectory(self, "选取模型文件夹", "C:/", QFileDialog.ShowDirsOnly)
        self.exportInfo["导出路径"] = ExportPath
        return ExportPath


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win =  GetList()
    win.show()
    app.exec_()