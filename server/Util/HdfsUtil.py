# import hadoopy
# import pyhdfs
from hdfs3 import HDFileSystem
import logging
from configs import settings
import os

hdfs=HDFileSystem(host="127.0.0.1",port=9000)

def writeToHDFS(localpath,hdfspath):
    try:
        hdfs.put(localpath,hdfspath)
    except Exception as e:
        logging.exception(e)
        return False
    return True

def copyFromHDFS(sourceMapfilePath,localDistPath):
    try:
        hdfs.get(sourceMapfilePath,localDistPath)
    except Exception as e:
        logging.exception(e)
        return False
    return True

# if __name__ == "__main__":
    # localpath="/home/huawei/words"
    # hdfspath="/test/words"
    # writeToHDFS(localpath,hdfspath)

    # remotepath="/test/words"
    # localdistpath="/home/huawei/words"
    # copyFromHDFS(remotepath,localdistpath)
