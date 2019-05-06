import requests
import json
import os
import logging

def Get_AllTables(URL,header,proxy):
    try:
        r = requests.get(URL, headers=header, proxies=proxy)
        if (r.status_code == 200):
            table_list=json.loads(r.text)
            return table_list
        else:
            return 1
    except Exception as e:
        logging.exception(e)
        return 1




def Get_FieldAndItems(URL,header,proxy,table):
    # URL_table=os.path.join(URL,table)
    URL_table=URL+"/"+table
    try:
        r = requests.get(URL_table, headers=header, proxies=proxy)
        if (r.status_code == 200):
            field_dict=json.loads(r.text)
            return field_dict
        else:
            return 1
    except Exception as e:
        logging.exception(e)
        return 1

def GetNamesByOption(URL,option):
    try:
        r = requests.post(URL, data=option)
        if (r.status_code == 200):
            return json.loads(r.text)
        else:
            return 1
    except Exception as e:
        logging.exception(e)
        return 1

def DeleteTarFile(URL,header,proxy):
    try:
        r = requests.get(URL, headers=header, proxies=proxy)
        if (r.status_code == 200):
            return 0

            # return (r.text)
        else:
            return 1
    except Exception as e:
        logging.exception(e)
        return 1

def GetImageByName(URL, data_name, store_path):
    try:
        r = requests.post(URL, data=data_name)
        if (r.status_code == 200):
            with open(store_path,'wb') as file:
                file.write(r.content)
            return (0)
        else:
            return 1
    except Exception as e:
        logging.exception(e)
        return 1

def GetImageByName3(URL,data_name,store_path):
    try:
        r = requests.post(URL, data=data_name)
        if (r.status_code == 200):
            with open(store_path, 'wb') as file:
                file.write(r.content)
            return 0

            # return (r.text)
        else:
            return 1
    except Exception as e:
        logging.exception(e)
        return 1

def GetImageByName2(URL,img_name,folder_name):
    try:
        data={}
        data['image_name']=img_name
        r = requests.post(URL, data=data)
        if (r.status_code == 200):
            if (r.text != "1"):
                file_name=os.path.join(folder_name,img_name)
                # with open(file_name, 'wb') as file:
                #     file.write(r.content)
                return 0
            else:
                return 1

        else:
            return 1
    except Exception as e:
        logging.exception(e)
        return 1

def GetSizeByName(URL,data_name):
    try:
        r = requests.post(URL, data=data_name)
        if (r.status_code == 200):
            return json.loads(r.text)
            # return (r.text)
        else:
            return 1
    except Exception as e:
        logging.exception(e)
        return 1


if __name__=="__main__":
    headers = {
        'User - Agent': 'Mozilla / 5.0(Windows NT 6.1;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 70.0.3538.110Safari / 537.36',
        'Connection': 'close'
    }
    proxies = {
        'http': None, 'https': None
    }
    # QUERY_URL = "http://10.101.170.80:50007/table_query"
    # AllTables=Get_AllTables(QUERY_URL,header=headers,proxy=proxies)
    # if (AllTables != 0):
    #     print (AllTables)
    # else:
    #     print (u"连接服务器失败")

    # table_name="WirelessAOI"
    # QUERY_URL="http://10.101.170.80:50007/table_field_query"
    # FieldAndItems=Get_FieldAndItems(QUERY_URL,header=headers,proxy=proxies,table=table_name)
    # print (FieldAndItems)

    POST_URL1 = "http://10.101.170.80:50007/image_query_by_option"
    # option={'table_name':'abc','field_option':'cde'}
    option={}
    option['table_name']='WirelessAOI'
    field_option={}
    field_option['board_id']='02312KWN'
    field_option['mission_id']='HK2'
    field_option['label']='OK'
    field_option['time_point']=['20190327','20190328']
    option["field_option"]=json.dumps(field_option)
    print (option)
    image_names=GetNamesByOption(POST_URL1,option)
    for image_name in image_names:
        print (image_name)

    POST_URL2="http://10.101.170.80:50007/get_image_by_name"
    data={}
    data['image_names']=json.dumps(image_names)
    status=GetImageByName(POST_URL2,data)
    print (status)


