import shutil
from os.path import join
import os

import logging

#move files from directory to directory
def moveImages(images,srcFolder,dstFolder):
    try:
        for name in images:
            srcFilePath=join(srcFolder,name)
            move(srcFilePath,dstFolder)
    except Exception as e:
        logging.exception(e)
        return False
    return True

#move file from path to path
def move(src,dst):
    try:
        shutil.move(src,dst)
    except Exception as e:
        if type(e)!=shutil.Error:
            logging.exception(e)
        return False
    return True

#copy file from path to path
def copy(srcFilePath,dstFilePath):
    try:
        shutil.copy(srcFilePath,dstFilePath)
    except Exception as e:
        logging.exception(e)
        return False
    return True

#remove file
def removeFile(path):
    try:
        os.remove(path)
    except Exception as e:
        logging.exception(e)
        return False
    return True

#remove folder
def removeFolder(path):
    try:
        shutil.rmtree(path)
    except Exception as e:
        logging.exception(e)
        return False
    return True

#detect thether the file is exist
def exists(path):
    try:
        flag=os.path.exists(path)
    except Exception as e:
        logging.exception(e)
        flag=False
    return flag

def getAbsolutePaths(names,folder_path):
    results=None
    try:
        results=[os.path.join(folder_path,name) for name in names]
    except Exception as e:
        logging.exception(e)
        return False
    return results

#create folder
def mkdir(path):
    try:
        os.mkdir(path)
    except Exception as e:
        logging.exception(e)
        return False
    return True

#create recursive folder
def makedirs(folder):
    try:
        os.makedirs(folder)
    except Exception as e:
        logging.exception(e)
        return False
    return True

if __name__=='__main__':
    # copy('/home/huawei/image_server/3.txt','/home/huawei/image_server/test_dir/222.txt')
    move('/home/huawei/image_server/test_dir/222.txt','/home/huawei/image_server/')