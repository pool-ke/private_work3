from configs import settings
from Util import RedisUtil
# from Util import MapFileUtil
from Util import ScpUtil
from Util import FileUtil
from Util import CassandraUtil
# from Util import MysqlUtil
from Util import MysqlUtil2 as MysqlUtil
from Util import MysqlUtil3
from Util import CassandraUtil3
import os
import time
import json
import logging
import uuid

#logging setting
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)s:%(funcName)s] %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
)

class Server:
    def __init__(self,prepare_dir,queue_dir):
        self.prepare_dir=prepare_dir
        self.queue_dir=queue_dir
        self.num=100

    #get the file size of the files
    def _getImagesTotalSize(self,imagePaths):
        return sum(os.path.getsize(os.path.join(self.prepare_dir,path.decode("utf-8"))) for path in imagePaths)

    

    def _transfer(self,size):
        images=RedisUtil.pop(self.num,"prepare")
        images=[image.decode("utf-8") for image in images]
        print (images)
        if images:
            if RedisUtil.push(images,"image") and RedisUtil.addSize(size):
                if FileUtil.moveImages(images,self.prepare_dir,self.queue_dir):
                    return True
        return False

    def run(self,time_interval):
        #check the setting files to create new tables in the first time before running
        MysqlUtil.create_all_tables()
        #run server as polling task
        while(1):
            #sleep for a few second
            time.sleep(time_interval)
            preImageNames=RedisUtil.get(self.num,"prepare")
            if preImageNames is None or len(preImageNames)==0:
                # logging.info("wait for images in PreQueue")
                continue
            #get the image names and the relative fields in json
            preImageNames=RedisUtil.pop(self.num,"prepare")
            preImageJsons=RedisUtil.pop(self.num,"json_prepare")
            preImageNames=[image.decode("utf-8") for image in preImageNames]
            preImageJsons=[image.decode("utf-8") for image in preImageJsons]
            if (len(preImageNames) != len(preImageJsons)):
                logging.info("The num of preImages of preImageJson is error")
            MysqlUtil.reconnect()
            for i in range(len(preImageNames)):
                logging.info(preImageNames[i])
                info_dict=json.loads(preImageJsons[i])
                image_path=os.path.join(settings.prepare_dir,preImageNames[i])
                if os.path.exists(image_path):
                    # insert_data=(info_dict['file_name'],info_dict['product_type'],info_dict['device_type'],info_dict['label'],info_dict['board_id'],info_dict['board_loc'],info_dict['time'])
                    if info_dict['work_type']=='BoardAOI':
                        insert_data=(info_dict['file_name'],info_dict['device_id'],info_dict['time'],info_dict['product_type'],info_dict['board_id'],info_dict['component_type'],info_dict['board_loc'],info_dict['label'])
                    elif info_dict['work_type']=='WirelessAOI':
                        insert_data=(info_dict['file_name'],info_dict['board_id'],info_dict['mission_id'],info_dict['time_point'],info_dict['label'])
                    # MysqlUtil.insert_into_table_aoi_image(insert_data)
                    MysqlUtil.insert_into_table_aoi_image(info_dict['work_type'],insert_data)
                    #convert the image data into bytearray
                    image_data=bytearray(open(image_path,'rb').read())
                    CassandraUtil.insert_into_image_table(preImageNames[i],image_data)
                    #remove the file in folder cache after inserted into mysql and cassandra
                    FileUtil.removeFile(image_path)

    #待完整
    def run2(self,time_interval):
        #check the setting files to create new tables in the first time before running
        #MysqlUtil.create_all_tables()
        #run server as polling task
        print("start run server...")
        while(1):

            

            #sleep for a few second
            time.sleep(time_interval)
            preImage_jsoninfo=RedisUtil.get(self.num,"json_prepare")
            #print("tepe(preImage_jsoninfo)",type(preImage_jsoninfo),len(preImage_jsoninfo))
            if preImage_jsoninfo is None or len(preImage_jsoninfo)==0:
                # logging.info("wait for images in PreQueue")
                continue
            #get the image names and the relative fields in json
            #preImageNames=RedisUtil.pop(self.num,"prepare")
            preImageJsons=RedisUtil.pop(self.num,"json_prepare")
            #preImageNames=[image.decode("utf-8") for image in preImageNames]
            preImageJsons=[image.decode("utf-8") for image in preImageJsons]
            #if (len(preImageNames) != len(preImageJsons)):
            #    logging.info("The num of preImages of preImageJson is error")
            MysqlUtil.reconnect()
            for i in range(len(preImageJsons)):
                info_dict=json.loads(preImageJsons[i])
                #print("info_dict:",info_dict)
                #info_dict['ImageName']=info_dict['ImageName']
                curr_image_name=info_dict['ImageName']
                #curr_image_type=info_dict['ProjectName']#未定
                logging.info(curr_image_name)
                
                image_path=os.path.join(settings.prepare_dir,curr_image_name)
                print("temp_image_path",image_path)
                
                
                if os.path.exists(image_path):
                    #print(image_path," exists!")
                    #dict_test={}#从json得出的字典

                    #UUID=uuid.uuid5(uuid.NAMESPACE_DNS, info_dict["ImageName"])
                    UUID=uuid.uuid1()
                    info_dict["Uuid"]=str(UUID)

                    # insert_data=(info_dict["Uuid"],info_dict["MachineId"],
                    # info_dict["ProjectName"],info_dict["ProductName"],
                    # info_dict["BarCode"],info_dict["ImageName"],
                    # info_dict["LabelType"],info_dict["Labels"],
                    # info_dict["GenerateDateTime"])

                    
                    
                    
                    jsonsavetofile=True#默认
                    CurrtableName=None#数据表名
                    if info_dict["LabelType"] in ["Detection","Segmentation"] and jsonsavetofile:
                        CurrtableName=info_dict['ProjectName']+"_Detection_Segmentation"
                    elif info_dict["LabelType"] in ["Detection","Segmentation"] and not jsonsavetofile:
                        CurrtableName=info_dict['ProjectName']+"_Detection_Segmentation_withjson"
                    elif info_dict["LabelType"] in ["Classification"]:
                        CurrtableName=info_dict['ProjectName']+"_Classification"
                    else:
                        CurrtableName=None
                        print("image's LabelType:",info_dict["LabelType"]," is error")
                        continue
                    print("Current TableName",CurrtableName)
                    #解析出ObjectType，ObjectName，label
                    curr_obj_type=""
                    curr_obj_name=""
                    curr_label=""
                    curr_labels_path=settings.mysql_json_file_dir
                    if not os.path.exists(curr_labels_path):
                        os.mkdir(curr_labels_path)
                    curr_labels_path=os.path.join(curr_labels_path,info_dict["ImageName"]+".json")
                    #对于分类任务，提取目标类型，目标名称，标签
                    #假设分类任务的标签是只有一个元素的字典列表
                    if info_dict["LabelType"] in ["Classification"]:
                        list_label_of_dic=list(info_dict['Labels'])
                        assert len(list_label_of_dic)==1
                        curr_obj_type=list_label_of_dic[0]["ObjectType"]
                        curr_obj_name=list_label_of_dic[0]["ObjectName"]
                        curr_label=list_label_of_dic[0]["label"]
                    #mysql 插入数据 以字典形式
                    CurrParamDict={}
                    CurrParamDict.update({"Uuid":info_dict["Uuid"]})
                    CurrParamDict.update({"MachineId":info_dict["MachineId"]})
                    CurrParamDict.update({"ProjectName": info_dict["ProjectName"]})
                    CurrParamDict.update({"ProductName":info_dict["ProductName"]})
                    CurrParamDict.update({"BarCode": info_dict["BarCode"]})
                    CurrParamDict.update({"ImageName":info_dict["ImageName"]})
                    CurrParamDict.update({"LabelType":info_dict["LabelType"]})
                    CurrParamDict.update({"Labels":info_dict["Labels"]})
                    CurrParamDict.update({"GenerateDateTime":info_dict["GenerateDateTime"]})
                    
                    CurrParamDict.update({"ObjectType":curr_obj_type})
                    CurrParamDict.update({"ObjectName":curr_obj_name})
                    CurrParamDict.update({"label":curr_label})
                    
                    CurrParamDict.update({"LabelsPath":curr_labels_path})
                    
                    #根据Project Name,LabelType 创建数据表，如果存在则不创建
                    MysqlUtil3.create_new_table_by_type_task(CurrtableName,info_dict["LabelType"])
                    
                    #把
                    #插入mysql数据
                    MysqlUtil3.insert_into_table_image_v2(CurrtableName,info_dict["LabelType"],CurrParamDict)
                    print("num ",i,"insert "+info_dict["ImageName"]+" into "+"mysql_table "+CurrtableName)

                    
                    #MysqlUtil3.insert_into_table_image_new(info_dict['ProjectName'],insert_data)
                    #convert the image data into bytearray
                    #print("begin insert cassandra...")
                    image_data=bytearray(open(image_path,'rb').read())
                    CassandraUtil3.insert_into_image_table_Uuid_Imagedata(str(UUID),image_data)#return no use
                    #CassandraUtil3.insert_into_image_table_withUuid(str(UUID),curr_image_name,image_data)
                    #remove the file in folder cache after inserted into mysql and cassandra
                    print("remove file...")
                    FileUtil.removeFile(image_path)
                    print("wait client...")
                else:
                    print(image_path," no exists")


if __name__=='__main__':
    server=Server(settings.prepare_dir,settings.queue_dir)
    server.run2(settings.time_interval)
    # preImageNames=RedisUtil.get(100,"prepare")
    # if preImageNames is None or len(preImageNames)==0:
    #     logging.info("wait for images in PreQueue")
    # preImageNames=RedisUtil.get(100,"prepare")
    # preImageJsons=RedisUtil.get(100,"json_prepare")
    # preImageNames=[image.decode("utf-8") for image in preImageNames]
    # preImageJsons=[image.decode("utf-8") for image in preImageJsons]
    # if (len(preImageNames) != len(preImageJsons)):
    #     logging.info("The num of preImages of preImageJson is error")
    # for i in range(len(preImageNames)):
    #     logging.info(preImageNames[i])
    #     info_dict=json.loads(preImageJsons[i])
    #     image_path=os.path.join(settings.prepare_dir,preImageNames[i])
    #     if os.path.exists(image_path):
    #         insert_data=(info_dict['file_name'],info_dict['product_type'],info_dict['device_type'],info_dict['label'],info_dict['board_id'],info_dict['board_loc'],info_dict['time'])
    #         MysqlUtil.insert_into_table_aoi_image(insert_data)
    #         image_data=bytearray(open(image_path,'rb').read())
    #         CassandraUtil.insert_into_image_table(preImageNames[i],image_data)
    #         # FileUtil.removeFile(image_path)