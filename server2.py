from configs import settings
from Util import RedisUtil
# from Util import MapFileUtil
from Util import ScpUtil
from Util import FileUtil
from Util import CassandraUtil
# from Util import MysqlUtil
from Util import MysqlUtil2 as MysqlUtil
import os
import time
import json
import logging

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
                logging.info("wait for images in PreQueue")
                continue
            #get the image names and the relative fields in json
            preImageNames=RedisUtil.pop(self.num,"prepare")
            preImageJsons=RedisUtil.pop(self.num,"json_prepare")
            preImageNames=[image.decode("utf-8") for image in preImageNames]
            preImageJsons=[image.decode("utf-8") for image in preImageJsons]
            if (len(preImageNames) != len(preImageJsons)):
                logging.info("The num of preImages of preImageJson is error")
            for i in range(len(preImageNames)):
                logging.info(preImageNames[i])
                info_dict=json.loads(preImageJsons[i])
                image_path=os.path.join(settings.prepare_dir,preImageNames[i])
                if os.path.exists(image_path):
                    # insert_data=(info_dict['file_name'],info_dict['product_type'],info_dict['device_type'],info_dict['label'],info_dict['board_id'],info_dict['board_loc'],info_dict['time'])
                    insert_data=(info_dict['file_name'],info_dict['device_id'],info_dict['time'],info_dict['product_type'],info_dict['board_id'],info_dict['component_type'],info_dict['board_loc'],info_dict['label'])
                    # MysqlUtil.insert_into_table_aoi_image(insert_data)
                    MysqlUtil.insert_into_table_aoi_image("aoiimage",insert_data)
                    #convert the image data into bytearray
                    image_data=bytearray(open(image_path,'rb').read())
                    CassandraUtil.insert_into_image_table(preImageNames[i],image_data)
                    #remove the file in folder cache after inserted into mysql and cassandra
                    FileUtil.removeFile(image_path)





2

if __name__=='__main__':
    server=Server(settings.prepare_dir,settings.queue_dir)
    server.run(settings.time_interval)
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