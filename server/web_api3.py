from flask import Flask,request,redirect,url_for,jsonify,send_from_directory,render_template,Response
from Util import RedisUtil
# from Util import MysqlUtil
#from Util import MysqlUtil2 as MysqlUtil
#from Util import CassandraUtil
#from Util import CompressUtil
from Util import MysqlUtil3 as MysqlUtil1
from Util import FileUtil
import sys
import os
# from configs import settings
import settings

# from configs import mysql_init
#import mysql_init
import json
import logging
import time
import base64

import ntpath


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)s:%(funcName)s] %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
)

ALLOWED_EXTENSIONS=set(['jpg','jpeg','JPG','JPEG','png','PNG','bmp','BMP'])
upload_path=settings.prepare_dir

app=Flask(__name__)

@app.route('/client_ipaddr')
def getIpAddr():
    ip_addr=request.remote_addr
    print (type(ip_addr))
    print (ip_addr)
    return ip_addr+ip_addr

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/hello/<name>/<words>',methods=['GET'])
def hello(name,words):
    return jsonify({'name':name,'words':words})#key=value jsonify(name=name,words=words)

# upload interface for the C# client
@app.route('/uploadfiles_test',methods=['POST'])
def uploadfiles_test_json():
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
            # if info_list[0]=="BoardAOI":
            #     dict_temp['work_type']=info_list[0]
            #     dict_temp['device_id']=info_list[1]
            #     dict_temp['time']=info_list[2][0:8]
            #     dict_temp['product_type']=info_list[3]
            #     dict_temp['board_id']=info_list[4]
            #     dict_temp['component_type']=info_list[5]
            #     dict_temp['board_loc']=info_list[6]
            #     dict_temp['label']=info_list[7]
            #     dict_temp['file_name']=file.filename
            # elif info_list[0]=="WirelessAOI":
            #     dict_temp['work_type']=info_list[0]
            #     dict_temp['board_id']=info_list[1]
            #     dict_temp['mission_id']=info_list[2]
            #     dict_temp['time_point']=info_list[3][0:8]
            #     dict_temp['label']=info_list[4]
            #     dict_temp['file_name']=file.filename
            
            full_path=os.path.join(upload_path,file.filename)
            with open(full_path,'wb') as save_file:
                save_file.write(image_content)
            RedisUtil.push(file.filename,kind='prepare')
            RedisUtil.push(json.dumps(dict_temp),kind="json_prepare")
    return "1111"


#接收json_001
@app.route('/calc_test', methods=['POST'])
def calc():
    #data_list = []
    data = json.loads(request.get_data(as_text=True))
    print("type(data)",type(data))
    # for key, value in data.items():
    #     if value == '':
    #         data[key] = 0
    # for key, value in data.items():
    #     if type(value) == str and value != 'i':
    #         data[key] = float(value)
 
    # for i in data['data_list']:
    #     new_dict = {}
    #     new_dict['r'] = float(i['r'])
    #     new_dict['d'] = float(i['d'])
    #     new_dict['n'] = float(i['n'])
    #     new_dict['n_2'] = float(i['n_2'])
    #     data_list.append(new_dict)
    print(data)
    #print(data_list)
    try:
        pass
        # result = light_calc.main(data['D'], data['q'], data['ls'], data['Lz'], data['Uz'], data['l'], data['u'], data['y'],
        #                      data['P'], data['h1'], data_list)
        # resp = make_response(result)
        # resp.headers['Content-Type'] = 'text/json'
        # return result
    except Exception as e:
        print(e)
        return '{"status":"500"}'

@app.route('/json2', methods=['POST'])
def student_add():
    # request.json 只能够接受方法为POST、Body为raw，header 内容为 application/json类型的数据：对应图1
    # json.loads(request.dada) 能够同时接受方法为POST、Body为 raw类型的 Text 
    # 或者 application/json类型的值：对应图1、2
    params = request.json if request.method == "POST" else request.args
    try:
        print("type(params)",type(params))
        #session = DBManager.get_session()
        #c = Class(name=params['name'])
        #session.add(c)
        #session.commit()
        #session.close()
        print(params['ImageName'])
    except Exception as e:
        logging.exception(e)
    return 'success'#jsonify(code=200, status=0, message='ok', data={})


@app.route("/flaskjson", methods=['POST'])
def login():
    print('#'*20,"get post",'#'*20)
    data = request.get_json()#request.json
    #print("type(data):",type(data))
    #print('#'*20,'解析json...')
    if 'MachineId' in data.keys():
        MachineId = data['MachineId']
    else:
        data['MachineId']=None
    if 'ProjectName' in data.keys():
        ProjectName = data['ProjectName']
    else:
        data['ProjectName']=None
    if 'ProductName' in data.keys():
        ProductName = data['ProductName']
    else:
        data['ProductName']=None
    if 'BarCode' in data.keys():
        BarCode = data['BarCode']
    else:
        data['BarCode']=None
    if 'ImageName' in data.keys():
        data['ImageName']=ntpath.basename(data['ImageName'])#windows
        data['ImageName']=os.path.basename(data['ImageName'])   # 
        ImageName =  data['ImageName']
        print("basename:",os.path.basename(data['ImageName']))
    else:
        data['ImageName']=None
    if 'LabelType' in data.keys(): 
        LabelType = data['LabelType']
    else:
        data['LabelType']=None
    if 'Labels' in data.keys():   
        Labels = data['Labels']
        jl_label=list(data['Labels'])#json.loads(data['Labels'])
        # print("type(jl_label",type(jl_label),len(jl_label))
    
        # for i,la in enumerate(jl_label):
        #     temdic=dict(la)
        #     print(i,"temdic len:",len(temdic))
        #     for k,v in temdic.items():
        #         print(k,"------>",v)
    else:
        data['Labels']=None
    #print('#'*20)
    if 'GenerateDateTime' in data.keys(): 
        GenerateDateTime = data['GenerateDateTime']
    else:
        data['GenerateDateTime']=None
    #ProjectName = data['ProjectName']
    if 'ImageRawData' in data.keys():    
        ImageRawData = data['ImageRawData']
        #print("type(ImageRawData):",type(ImageRawData))
        image_data = base64.b64decode(ImageRawData)
        #print("type(image_data):",type(image_data))
        
        
        curr_img_path=os.path.join(upload_path,data['ImageName'])#
        #'D:\\share_dir\\ai_image_platform\\server\\abc.bmp'
        with open(curr_img_path,'wb') as fi:
            fi.write(image_data)
        del data['ImageRawData'] 
    else:
        data['ImageRawData']=None
        



    #RedisUtil.push(file.filename,kind='prepare')

    RedisUtil.push(json.dumps(data),kind="json_prepare")


    #print('#'*20,"\nget data:",data)

    return_response={}
    return_response["obj"]="success"
    return_response["errorCode"]=0
    return_response["errorMessage"]="ok"
    return_response["isSuccess"]=1#True

    return jsonify(return_response)#'{\"obj\":\"success\",\"errorCode\":0,\"errorMessage\":\"ok\",\"isSuccess\":true}'#u'返回元组', 200, {"name": "Warren"}#('success',0,'mess',True)#'#jsonify(data) # 返回布尔值


if __name__=='__main__':
    app.run(host=settings.api_host,port=8888,debug=True,threaded=False)