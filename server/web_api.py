from flask import Flask,request,redirect,url_for,jsonify,send_from_directory,render_template
from Util import RedisUtil
# from Util import MysqlUtil
from Util import MysqlUtil2 as MysqlUtil
from Util import CassandraUtil
from Util import CompressUtil
from Util import FileUtil
import sys
import os
from configs import settings
from configs import mysql_init
import json
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)s:%(funcName)s] %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
)

ALLOWED_EXTENSIONS=set(['jpg','jpeg','JPG','JPEG','png','PNG','bmp','BMP'])
upload_path=settings.prepare_dir

app=Flask(__name__)

#check filename in image format
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

#interface for testing
@app.route('/post_test',methods=['POST'])
def test():
    name=request.form.get("name")
    Id=request.form.get("id")
    job=request.form.get("job")
    dict_info={}
    dict_info["name"]=name
    dict_info["id"]=Id
    dict_info["job"]=job
    return json.dumps(dict_info)

# upload interface for the C# client
@app.route('/uploadfiles_test',methods=['POST'])
def uploadfiles_test():
    len=int(request.form.get("num_files"))
    print (len)
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    for i in range(len):
        file=request.files[str(i)]
        print (file.filename)
        if file and allowed_file(file.filename):
            image_content=file.stream.read()
            info_list=file.filename.split(".")[0].split("_")
            dict_temp={}
            if info_list[0]=="BoardAOI":
                dict_temp['work_type']=info_list[0]
                dict_temp['device_id']=info_list[1]
                dict_temp['time']=info_list[2][0:8]
                dict_temp['product_type']=info_list[3]
                dict_temp['board_id']=info_list[4]
                dict_temp['component_type']=info_list[5]
                dict_temp['board_loc']=info_list[6]
                dict_temp['label']=info_list[7]
                # dict_temp['device_id']=info_list[0]
                # dict_temp['time']=info_list[1][0:8]
                # dict_temp['product_type']=info_list[2]
                # dict_temp['board_id']=info_list[3]
                # dict_temp['component_type']=info_list[4]
                # dict_temp['board_loc']=info_list[5]
                # dict_temp['label']=info_list[6]
                # dict_temp['product_type']=info_list[0]
                # dict_temp['time']=info_list[1]
                # dict_temp['device_type']=info_list[2]
                # dict_temp['label']=info_list[3]
                # dict_temp['board_id']=info_list[4]
                # dict_temp['board_loc']=info_list[5]
                dict_temp['file_name']=file.filename
            elif info_list[0]=="WirelessAOI":
                dict_temp['work_type']=info_list[0]
                dict_temp['board_id']=info_list[1]
                dict_temp['mission_id']=info_list[2]
                dict_temp['time_point']=info_list[3][0:8]
                dict_temp['label']=info_list[4]
                dict_temp['file_name']=file.filename
            
            full_path=os.path.join(upload_path,file.filename)
            with open(full_path,'wb') as save_file:
                save_file.write(image_content)
            RedisUtil.push(file.filename,kind='prepare')
            RedisUtil.push(json.dumps(dict_temp),kind="json_prepare")
    return "1111"

#----------------------------------------------------------
# upload interface json格式 by dengqifeng
@app.route('/upload_json',methods=['POST'])
def upload_images_json():
    ##接收json数据 解析####################################
    ##### 每次读取几个json?
    len=int(request.form.get("num_files"))
    info_json=request.form.get("info_json")
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    
         
    imgs_info=json.loads(info_json)
    for obj_dict in imgs_info:
        file_name=obj_dict['ImageName']
        #image_type=obj_dict['ProjectName']
        image_byte_str=obj_dict['ImageRawData']
        #解码成图像字节
        #-----------
        image_content=image_byte_str
        #-----------

        full_path=os.path.join(upload_path,file_name)
        with open(full_path,'wb') as save_file:
            save_file.write(image_content)
        del obj_dict['ImageRawData']

        #if os.path.exists(file_path):
            #RedisUtil.push(file_name,kind="prepare")
        RedisUtil.push(json.dumps(obj_dict),kind="json_prepare")

    # print (len(imgs_info))
    return "1111"



@app.route('/',methods=['GET'])
def index():
    # return app.send_static_file('index.html')
    return render_template('index.html', visible_flag1 = "display:none;", visible_flag2 = "display:none;")

# upload interface for the browser client
@app.route('/infer',methods=['POST'])
def infer_images():
    files = request.files.getlist("files")
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    for file in files:
        print (file.filename)
        if file and allowed_file(file.filename):
            image_content=file.stream.read()
            info_list=file.filename.split("_")
            dict_temp={}
            dict_temp['product_type']=info_list[0]
            dict_temp['time']=info_list[1]
            dict_temp['device_type']=info_list[2]
            dict_temp['label']=info_list[3]
            dict_temp['board_id']=info_list[4]
            dict_temp['board_loc']=info_list[5]
            dict_temp['file_name']=file.filename
            full_path=os.path.join(upload_path,file.filename)
            with open(full_path,'wb') as save_file:
                save_file.write(image_content)
            RedisUtil.push(file.filename,kind='prepare')
            RedisUtil.push(json.dumps(dict_temp),kind="json_prepare")
    return "1111"

# upload interface for the python client
@app.route('/upload',methods=['POST'])
def upload_images():
    len=int(request.form.get("num_files"))
    info_json=request.form.get("info_json")
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    for i in range(len):
        file=request.files[str(i)]
        print (file.filename)
        if file and allowed_file(file.filename):
            image_content=file.stream.read()
            full_path=os.path.join(upload_path,file.filename)
            with open(full_path,'wb') as save_file:
                save_file.write(image_content)
    
    imgs_info=json.loads(info_json)
    for obj_dict in imgs_info:
        file_name=obj_dict['file_name']
        file_path=os.path.join(upload_path,file_name)
        if os.path.exists(file_path):
            RedisUtil.push(file_name,kind="prepare")
            RedisUtil.push(json.dumps(obj_dict),kind="json_prepare")

    # print (len(imgs_info))
    return "1111"

#query interface in browser by product_type ,component type,return the compressed file to the client
@app.route('/image_query/device_type/<query_str>')
def getImage1(query_str):
    querys=query_str.split('_')
    image_type=querys[0]
    product_type=querys[1]
    component_type=querys[2]
    dst_name=product_type+"_"+component_type
    results=MysqlUtil.execute_select_all_by_type(image_type,product_type,component_type)
    results=[result[0] for result in results]
    response_str=json.dumps(results)
    makeFilesToTar(results,dst_name)
    send_file_name=dst_name+".tar.bz2"
    return send_from_directory(settings.dstfile_dir,send_file_name,as_attachment=True)
    
#query interface in browser by product_type ,component type,label,return the compressed file to the client
@app.route('/image_query/defection_type/<query_str>')
def getImage2(query_str):
    querys=query_str.split('_')
    image_type=querys[0]
    product_type=querys[1]
    device_type=querys[2]
    defection_type=querys[3]
    dst_name=product_type+"_"+device_type+"_"+defection_type
    results=MysqlUtil.execute_select_all_by_defection_type(image_type,product_type,device_type,defection_type)
    results=[result[0] for result in results]
    response_str=json.dumps(results)
    makeFilesToTar(results,dst_name)
    send_file_name=dst_name+".tar.bz2"
    return send_from_directory(settings.dstfile_dir,send_file_name,as_attachment=True)

#query interface in browser by product_type ,component type,label,time_point,return the compressed file to the client
@app.route('/image_query/time_point/<query_str>')
def getImage3(query_str):
    querys=query_str.split('_')
    image_type=querys[0]
    product_type=querys[1]
    device_type=querys[2]
    defection_type=querys[3]
    time_point=querys[4]
    dst_name=product_type+"_"+device_type+"_"+defection_type+"_"+time_point
    results=MysqlUtil.execute_select_all_by_time(image_type,product_type,device_type,defection_type,time_point)
    results=[result[0] for result in results]
    response_str=json.dumps(results)
    makeFilesToTar(results,dst_name)
    send_file_name=dst_name+".tar.bz2"
    return send_from_directory(settings.dstfile_dir,send_file_name,as_attachment=True)

@app.route('/table_query')
def getTables():
    MysqlUtil.reconnect()
    return json.dumps(mysql_init.table_name)

@app.route('/table_field_query/<table_name>')
def getTableField(table_name):
    Res_FieldAndItems={}
    fields=mysql_init.table_inits[table_name].keys()
    for field in fields:
        if (field not in ["image_name","time_point"]):
            items=MysqlUtil.Find_Items(table_name,field)
            Res_FieldAndItems[field]=[item[0] for item in items]
    return json.dumps(Res_FieldAndItems)

@app.route('/client_ipaddr')
def getIpAddr():
    ip_addr=request.remote_addr
    print (type(ip_addr))
    print (ip_addr)
    return ip_addr

@app.route('/image_query_by_option',methods=['POST'])
def image_query_by_option():
    table_name=request.form.get("table_name")
    field_option=json.loads(request.form.get("field_option"))
    imagenames=MysqlUtil.Find_imagenames(table_name,field_option)
    imagenames=[imagename[0] for imagename in imagenames]
    return json.dumps(imagenames)

@app.route('/get_image_by_name2',methods=['POST'])
def get_image_by_name2():
    image_names=json.loads(request.form.get("image_names"))
    for image in image_names:
        print (image)
    # return "111"
    dst_name=request.remote_addr
    folder_name2=dst_name+"_2"
    folder_name1=os.path.join(settings.dstfile_dir,dst_name)
    folder_name2=os.path.join(settings.dstfile_dir,folder_name2)
    dst_name=dst_name+".pkl"
    makeFilesToPKL(image_names,dst_name,folder_name1,folder_name2)
    send_file_name=dst_name
    return send_from_directory(settings.dstfile_dir,send_file_name,as_attachment=True)

@app.route('/get_image_by_name',methods=['POST'])
def get_image_by_name():
    image_names=json.loads(request.form.get("image_names"))
    for image in image_names:
        print (image)
    # return "111"
    dst_name=request.remote_addr
    makeFilesToTar(image_names,dst_name)
    send_file_name=dst_name+".tar.bz2"
    # return send_from_directory(settings.dstfile_dir,send_file_name,as_attachment=True)
    return "111"

@app.route('/find_image_by_name',methods=['POST'])
def find_image_by_name():
    image_name=request.form.get("image_name")
    print (image_name)
    # return "111"
    folder_name=request.remote_addr
    folder_name=os.path.join(settings.dstfile_dir,folder_name)
    status=makeFileToFolder(image_name,folder_name)
    if status ==1:
        logging.info("the image:%s is not exist!",image_name)
        return "1"
    else:
        send_file_name=image_name
        return send_from_directory(folder_name,send_file_name,as_attachment=True)

@app.route('/get_size_by_name',methods=['POST'])
def get_size_by_name():
    image_names=json.loads(request.form.get("image_names"))
    folder_name=request.remote_addr
    folder_name=os.path.join(settings.dstfile_dir,folder_name)
    getImageToLFS(image_names,folder_name)
    size_dict=getSizeOfImages(folder_name)
    return size_dict


@app.route('/delete_tarfile',methods=['GET'])
def delete_tarfile():
    dst_name=request.remote_addr
    send_file_name=dst_name+".pkl"
    tar_file=os.path.join(settings.dstfile_dir,send_file_name)
    if (FileUtil.exists(tar_file)):
        FileUtil.removeFile(tar_file)
        print("delete "+dst_name+ " pklfile successfully")
    folder_name=os.path.join(settings.dstfile_dir,dst_name)
    if (FileUtil.exists(folder_name)):
        FileUtil.removeFolder(folder_name)
        print("delete "+folder_name+ " tarfile successfully")
    return "OK"

@app.route('/delete_folder',methods=['GET'])
def delete_cache_folder():
    dst_name=request.remote_addr
    if (FileUtil.exists(dst_name)):
        FileUtil.removeFolder(dst_name)
        print("delete folder "+dst_name+ " tarfile successfully")
    return "OK"

#compress the folder into conpressed file and remove it to svae the space of filesystem
def makeFilesToTar(results,dst_name):
    if not FileUtil.exists(settings.query_dir):
        FileUtil.mkdir(settings.query_dir)
    for result_name in results:
        logging.info(result_name)
        image_result=CassandraUtil.select_by_image_name(result_name)
        if image_result is not None:
            save_path=os.path.join(settings.query_dir,result_name)
            open(save_path,'wb').write(image_result)
        else:
            logging.info("the image:%s is not exist!",result_name)
    tar_path=os.path.join(settings.dstfile_dir,dst_name)
    CompressUtil.CompressFiletoTar2(SourceFolder=settings.query_dir,DstFile=tar_path)
    FileUtil.removeFolder(settings.query_dir)

def makeFilesToTar2(results,dst_name,folder_name1,folder_name2):
    if not FileUtil.exists(folder_name2):
        FileUtil.mkdir(folder_name2)
    for result_name in results:
        file_path1=os.path.join(folder_name1,result_name)
        file_path2=os.path.join(folder_name2,result_name)
        FileUtil.move(file_path1,file_path2)
    tar_path=os.path.join(settings.dstfile_dir,dst_name)
    CompressUtil.CompressFiletoTar2(SourceFolder=folder_name2,DstFile=tar_path)
    FileUtil.removeFolder(folder_name2)

def makeFilesToPKL(results,dst_name,folder_name1,folder_name2):
    if not FileUtil.exists(folder_name2):
        FileUtil.mkdir(folder_name2)
    for result_name in results:
        file_path1=os.path.join(folder_name1,result_name)
        file_path2=os.path.join(folder_name2,result_name)
        FileUtil.move(file_path1,file_path2)
    tar_path=os.path.join(settings.dstfile_dir,dst_name)
    CompressUtil.CompressFileToPKL(SourceFolder=folder_name2,DstFile=tar_path)
    FileUtil.removeFolder(folder_name2)

def getImageToLFS(results,folder_name):
    if not FileUtil.exists(folder_name):
        FileUtil.mkdir(folder_name)
    for result_name in results:
        logging.info(result_name)
        image_result=CassandraUtil.select_by_image_name(result_name)
        if image_result is not None:
            save_path=os.path.join(folder_name,result_name)
            open(save_path,'wb').write(image_result)
        else:
            logging.info("the image:%s is not exist!",result_name)
    # tar_path=os.path.join(settings.dstfile_dir,dst_name)
    # CompressUtil.CompressFiletoTar2(SourceFolder=settings.query_dir,DstFile=tar_path)
    # FileUtil.removeFolder(settings.query_dir)

def getSizeOfImages(folder):
    size_dict={}
    AllImages=os.listdir(folder)
    for image in AllImages:
        file_path=os.path.join(folder,image)
        size_dict[image]=os.path.getsize(file_path)
    return json.dumps(size_dict)
        

def makeFileToFolder(image_name,folder_name):
    if not FileUtil.exists(folder_name):
        FileUtil.mkdir(folder_name)
    image_result=CassandraUtil.select_by_image_name(image_name)
    if image_result is not None:
        save_path=os.path.join(folder_name,image_name)
        open(save_path,'wb').write(image_result)
        return 0
    else:
        logging.info("the image:%s is not exist!",image_name)
        return 1
    
        

if __name__=='__main__':
    app.run(host=settings.api_host,port=settings.api_port,debug=settings.api_debug_flag,threaded=settings.api_threaded)