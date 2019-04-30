#tar -jcv -f filename.tar.bz2 +打包的文件名 使用bzip2压缩
#tar -zcv -f filename.tar.gz +打包的文件名 使用gzip压缩
#tar -Jcv -f filename.tar.xz +打包的文件名 使用xz进行压缩
#tar -jtv -f filename.tar.bz2 查看打包的文件
#tar -jxv -f filename.tar.bz2 -C 要解压缩的目录 解压bzip2压缩的文件

#only supported in non-share directory

import os
import logging
import tensorflow as tf
from PIL import Image
from shutil import make_archive
from shutil import unpack_archive

#method1:use the native shell
def CompressFiletoTar(SourceFolder,DstFile,method="bz2"):
    if SourceFolder[-1]!='/':
        SourceFolder=os.path.join(SourceFolder,'/')
    print(SourceFolder)
    if method=="bz2":
        cmd_str="tar -jcv -f "+DstFile+".tar.bz2"+" "+SourceFolder+"*"
    elif method=="gz":
        cmd_str="tar -zcv -f "+DstFile+".tar.gz"+" "+SourceFolder+"*"
    elif method=="xz":
        cmd_str="tar -Jcv -f "+DstFile+".tar.xz2"+" "+SourceFolder+"*"
    else:
        return False
    print(cmd_str)
    try:
        os.system(cmd_str)
    except Exception as e:
        logging.info(e)
    return True

#ust shutil api to compress
def CompressFiletoTar2(SourceFolder,DstFile,method="bz2"):#ust shutil api to compress
    print (SourceFolder)
    # SourceFolder+='*'
    if method=="bz2":
        method_para='bztar'
    elif method=="gz":
        method_para='gztar'
    elif method=="xz":
        method_para='xztar'
    else:
        return False
    try:
        print (111)
        new_path=make_archive(DstFile,method_para,SourceFolder)
        print (new_path)
    except Exception as e:
        logging.info(e)
    return True

#use shutil api to uncompress
def UnCompressTartoFolder(SourceFile,DstFolder):#use shutil api to compress
    # print (SourceFolder)
    # # SourceFolder+='*'
    # if method=="bz2":
    #     method_para='bztar'
    # elif method=="gz":
    #     method_para='gztar'
    # elif method=="xz":
    #     method_para='xztar'
    # else:
    #     return False
    try:
        print (111)
        unpack_archive(SourceFile,DstFolder)

    except Exception as e:
        logging.info(e)
    return True

#compress files into tfrecords
def CompressFiletoTFRecords(SourceFolder,DstFile,img_W,img_H):
    if SourceFolder[-1]!='/':
        SourceFolder=SourceFolder.join('/')
    index=0#default label
    writer = tf.python_io.TFRecordWriter(DstFile)
    for image in os.listdir(SourceFolder):
        if image.split('.')[-1] in ["jpg","png","jgep","bmp"]:
            img_path=SourceFolder+image
            print(img_path)
            img = Image.open(img_path).convert("L")
            img = img.resize((img_W,img_H))
            img_raw = img.tobytes()#transform image to byte
            example = tf.train.Example(features = tf.train.Features(feature={
                    "label": tf.train.Feature(int64_list = tf.train.Int64List(value = [index])),
                    "img_raw": tf.train.Feature(bytes_list = tf.train.BytesList(value = [img_raw]))}))
            writer.write(example.SerializeToString())
    writer.close()


if __name__ =="__main__":
    # Folder="/home/huawei/image_server/flasktest/imgtest/"
    # file="/home/huawei/image_server/test001"
    # CompressFiletoTar2(SourceFolder=Folder,DstFile=file)

    file="/home/huawei/image_server/test001.tar.bz2"
    Folder="/home/huawei/image_server/test_dir2"
    UnCompressTartoFolder(SourceFile=file,DstFolder=Folder)
    # W=138
    # H=323
    # Folder="/home/huawei/image_server/flasktest/imgtest/"
    # file="/home/huawei/image_server/test001.tfrecords"
    # CompressFiletoTFRecords(SourceFolder=Folder,DstFile=file,img_W=W,img_H=H)
