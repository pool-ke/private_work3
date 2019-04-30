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
import json
import logging

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
            # dict_temp={'work_type'}=info_list[0]
            dict_temp['device_id']=info_list[0]
            dict_temp['time']=info_list[1][0:8]
            dict_temp['product_type']=info_list[2]
            dict_temp['board_id']=info_list[3]
            dict_temp['component_type']=info_list[4]
            dict_temp['board_loc']=info_list[5]
            dict_temp['label']=info_list[6]
            # dict_temp['product_type']=info_list[0]
            # dict_temp['time']=info_list[1]
            # dict_temp['device_type']=info_list[2]
            # dict_temp['label']=info_list[3]
            # dict_temp['board_id']=info_list[4]
            # dict_temp['board_loc']=info_list[5]
            dict_temp['file_name']=file.filename
            full_path=os.path.join(upload_path,file.filename)
            with open(full_path,'wb') as save_file:
                save_file.write(image_content)
            RedisUtil.push(file.filename,kind='prepare')
            RedisUtil.push(json.dumps(dict_temp),kind="json_prepare")
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

if __name__=='__main__':
    app.run(host=settings.api_host,port=settings.api_port,debug=settings.api_debug_flag)