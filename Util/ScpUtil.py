import sys
sys.path.append("../configs")
sys.path.append("configs")
import settings

import paramiko,datetime,os

hostname=settings.server_host
username=settings.ssh2_username
password=settings.ssh2_passwd
port=settings.ssh2_port

def _transferFiles(local_dir,remote_dir,remote_prefix="",flag="get"):
    try:
        #connect to another machine in linux or connect to another docker in on machine,in order to construct distributed system
        t=paramiko.Transport((hostname,port))
        t.connect(username=username,password=password)
        sftp=paramiko.SFTPClient.from_transport(t)
        if flag=="get":
            files=sftp.listdir(remote_dir)
        else:
            files=sftp.listdir(local_dir)
            
        #traver in folder
        for f in files:
            print (f)
            if f.split(".")[-1] not in ["jpg","png","jgep","bmp"]:
                continue
            #get or put the file from one machine to another machine with the file path
            if flag=="get":
                sftp.get(os.path.join(remote_dir,f),os.path.join(local_dir,f))
            else:
                sftp.put(os.path.join(local_dir,f),os.path.join(remote_dir,remote_prefix+"-"+f))
        t.close()
        return True
    except Exception as e:
        print (e)
        return False

def getFiles(remote_dir,local_dir):
    return _transferFiles(local_dir,remote_dir)

def putFiles(local_dir,remote_dir,remote_prefix=""):
    return _transferFiles(local_dir,remote_dir,remote_prefix,"put")

def _transferFile(local_path,remote_path,flag="get"):
    try:
        t=paramiko.Transport((hostname,port))
        t.connect(username=username,password=password)
        sftp=paramiko.SFTPClient.from_transport(t)
        if flag=="get":
            sftp.get(remote_path,local_path)
        else:
            sftp.put(local_path,remote_path)
        t.close()
        return True
    except Exception as e:
        print (e)
        return False

def getFile(remote_path,local_path):
    return _transferFile(local_path,remote_path,"get")

def putFile(local_path,remote_path):
    return _transferFile(local_path,remote_path,"put")

if __name__=="__main__":
    local_dir="/home/huawei/image_server/Pictures/"
    remote_dir="/home/huawei/1123PreImages/"
    putFiles(local_dir,remote_dir)

    # local_dir="/home/huawei/image_server/Pictures/"
    # remote_dir="/home/huawei/1123PreImages/"
    # getFiles(remote_dir,local_dir)

    