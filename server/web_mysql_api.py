from flask import Flask
from flask import request
from flask import send_file,send_from_directory
from werkzeug import secure_filename
from configs import settings

from Util import FileUtil
from Util import HBaseUtil
from Util import MapFileUtil
from Util import MysqlUtil
from os.path import join
import os

import json
import pickle
import logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)s:%(funcName)s] %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
)

Image_Folder="Upload_Images"

app=Flask(__name__,static_url_path='')

app.config['UPLOAD_FOLDER']='/home/huawei/image_server/flask_images'
app.config['ALLOWED_EXTENSIONS']= set(['png','jpg','jpeg','bmp'])

@app.route('/mysql_query/aoi_type/<query_str>')
def getImage1(query_str):
    results=MysqlUtil.execute_select_all_by_type(query_str)
    results=[result[0] for result in results]
    response_str=json.dumps(results)
    return response_str

@app.route('/mysql_query/defection_type/<query_str>')
def getImage2(query_str):
    querys=query_str.split('-')
    aoi_type=querys[0]
    defection_type=querys[1]
    results=MysqlUtil.execute_select_all_by_defection_type(aoi_type,defection_type)
    results=[result[0] for result in results]
    response_str=json.dumps(results)
    return response_str

@app.route('/mysql_query/time_point/<query_str>')
def getImage3(query_str):
    querys=query_str.split('-')
    aoi_type=querys[0]
    defection_type=querys[1]
    time_point=querys[2]
    results=MysqlUtil.execute_select_all_by_time(aoi_type,defection_type,time_point)
    results=[result[0] for result in results]
    response_str=json.dumps(results)
    return response_str

@app.route('/upload/images',methods=['POST'])
def upload_images():
    images_buffer_str=request.form['data']
    images_buffer_dict=pickle.loads(images_buffer_str)
    for key in images_buffer_dict.heys():
        priint (key)

@app.route('/register',methods=['POST'])
def register():
    print (request.form)
    print (request.form['name'])
    return "Hello World!"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload',methods=['POST'])
def upload():
    upload_dir=app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    upload_file=request.files['files']
    aoi_type=request.form.get('aoi_type')
    defection_type=request.form.get('defection_type')
    board_num=request.form.get('board_num')
    location_num=request.form.get('location_num')
    time_point=request.form.get('time_point')
    if upload_file and allowed_file(upload_file.filename):
        filename=secure_filename(upload_file.filename)
        upload_file.save(join(upload_dir,filename))
        insert_data=(filename,aoi_type,defection_type,board_num,location_num,time_point)
        MysqlUtil.insert_into_table_aoi_image(insert_data)
        return 'upload-'+filename+"success!"
    else:
        return 'upload-'+upload_file.file+"failed!"

# @app.route('/upload',methods=['POST'])
# def upload():
#     upload_files=request.files.getlist("files")
#     upload_dir=app.config['UPLOAD_FOLDER']
#     if not os.path.exists(upload_dir):
#         os.makedirs(upload_dir)
#     image_list=[]
#     for upload_file in files:
#         if upload_file and allowed_file(upload_file):
#             filename=secure_filename(upload_file.filename)
#             upload_file.save(upload_dir,filename)
#     return 'hello'+request.form.get('name')+"success!"

if __name__ == '__main__':
    app.run(host=settings.api_host,port=settings.api_port,debug=settings.api_debug_flag)