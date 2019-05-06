import sys
import os
from configs import settings
from os import listdir
from os.path import isfile,join
import pickle
import logging
from Util import FileUtil
from Util import HdfsUtil

PATH_NOT_EXISTS_MESSAGES="has exists in local file system"

def createMapFile(images,mapFilePath='temp'):
    try:
        dumpFilePath=os.path.join(settings.project_path,mapFilePath)
        dumpdict={}
        for path in images:
            with open(join(settings.queue_dir,path),'rb') as f:
                dumpdict[path]=f.read()
        with open(dumpFilePath,'wb') as f:
            f.write(pickle.dumps(dumpdict))
    except Exception as e:
        logging.exception(e)
        return False
    return True

def readMapFileFromHdfs(mapFileId):
    sourceMapFilePath=os.path.join(settings.images_hdfs_path,mapFileId)
    localDistPath=os.path.join(settings.mapfile_cache_folder,mapFileId)
    if HdfsUtil.copyFromHDFS(sourceMapFilePath,localDistPath):
        return readMapFile(mapFileId)
    else:
        return False

def readMapFile(mapFileId,imageCachePath=settings.images_cache_folder):
    sourceMapFilePath=os.path.join(settings.mapfile_cache_folder,mapFileId)
    if not FileUtil.exists(sourceMapFilePath):
        logging.error(sourceMapFilePath+PATH_NOT_EXISTS_MESSAGES)
        return False
    try:
        dir_path=imageCachePath
        if not FileUtil.exists(dir_path):
            FileUtil.mkdir(dir_path)
        with open(sourceMapFilePath,'rb') as f:
            dump_dict=pickle.loads(f.read())
        for key,value in dump_dict.items():
            imagepath=os.path.join(dir_path,key)
            with open(imagepath,'wb') as f:
                f.write(value)
    except Exception as e:
        logging.exception(e)
        return False
    return True