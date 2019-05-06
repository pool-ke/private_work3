#use the ftp and redis to test the function of the server
from Util import RedisUtil
from Util import ScpUtil
import settings
import os
import sys
sys.path.append("../configs")
sys.path.append("configs")
from configs import settings

def checkIfImage(basename):
    temp=basename.split(".")[-1]
    if temp in ["jpg","jpeg","png","bmp"]:
        return True
    return False

def filterImages(basenames):
    images=[s for s in basenames if checkIfImage(s)]
    return images

def putImagesToServer(path):
    if os.path.isfile(path):
        basename=os.path.basename(path)
        dirpath=os.path.dirname(path)
        dirname=os.path.split(dirpath)[1]

        basename=dirname+"-"+basename
        if checkIfImage(basename) and ScpUtil.putFile(path,os.path.join(settings.remote_dir,basename)):
            if RedisUtil.pushPre(basename):
                return True

    elif os.path.isdir(path):
        basenames=os.listdir(path)
        images=filterImages(basenames)
        dirname=os.path.split(path)[1]
        if dirname =="":
            dirname=os.path.split(os.path.split(path)[0])[1]
        print (dirname)
        images=[dirname+"-"+imageid for imageid in images]
        print (images)
        if ScpUtil.putFiles(path,settings.remote_dir,dirname):
            if RedisUtil.pushPre(images):
                return True
    
    else:
        print("image path is not right,neither a file or dir path")
    return False

def putImagesUpperFolder(folder_path):
    folders=os.listdir(folder_path)
    folders=[f for f in folders if os.path.listdir(os.path.join(folder,f))]
    for folder_path in folders:
        putImagesToServer(folder_path)

if __name__=="__main__":
    test_dir_path="/home/huawei/CAE_train_image/"
    putImagesToServer(test_dir_path)