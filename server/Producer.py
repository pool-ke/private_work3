import sys

from Util import MapFileUtil
from Util import RedisUtil
from Util import HBaseUtil
from Util import HdfsUtil
from Util import FileUtil
from Util import DumpFileUtil
# sys.path.append("../configs")
# sys.path.append("configs")
# sys.path.append("Util/hadoop/io")
# sys.path.append("Util/hadoop")
# sys.path.append("Util/hadoop/pydoop")
# sys.path.append("Util/")
# sys.path.append("Util/hadoop/util")

import pickle
import os
from os.path import join
# from Util.hadoop.io.IntWritable import LongWritable
# from Util.hadoop.io import MapFile
# from Util.hadoop.io import Text

import random
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)s:%(funcName)s] %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
)

MAX_MAPFILE_ID=1000000

class MapFileProducer:
    def __init__(self,images,settings):
        self.images=images
        self.mapFileId='1'
        self.settings=settings

    
    def _generateMapFileId(self):
        while True:
            self.mapFileId=str(random.randint(1,MAX_MAPFILE_ID))
            if not FileUtil.exists(self.mapFileId):
                break

    def _createMapFile(self):
        self._generateMapFileId()
        print (self.mapFileId)
        # return MapFileUtil.createMapFile(self.images,self.mapFileId)
        return DumpFileUtil.createMapFile(self.images,self.mapFileId)
    def _writeToHDFS(self):
        localpath=os.path.join(settings.project_path,self.mapFileId)
        hdfspath=os.path.join(settings.images_hdfs_path,self.mapFileId)
        print (localpath)
        print (hdfspath)
        return HdfsUtil.writeToHDFS(localpath,hdfspath)

    def _addRecord(self,db="hbase"):
        data={}
        for imageId in self.images:
            data[imageId]=self.mapFileId
        if db.lower()=="hbase":
            return HBaseUtil.put(data)
        elif db.lower()=="redis":
            return RedisUtil.hmsetImageToMapfile(data)
        else:
            logging.error("db type error,only can choose 'hbase' or 'redis' now")
            return False
    def run(self):
        if self._createMapFile():
            if self._writeToHDFS() and self._addRecord():
                dir_path=os.path.join(settings.project_path,self.mapFileId)
                if FileUtil.removeFile(dir_path):
                    return True
        else:
            logging.error("fail to produce mapfile")
            return False

from configs import settings
if __name__ =="__main__":
    producer=MapFileProducer(["111.bmp"],settings)
    if producer.run():
        logging.info("produce a mapfile success")