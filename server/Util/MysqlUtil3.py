


import sys
sys.path.append("../configs")
sys.path.append("configs")
import settings
import mysql_init
import pymysql
import logging
import datetime
import uuid
import json
#connect to the mysql server
db=pymysql.connect(host=settings.mysql_host,user=settings.mysql_user,password=settings.mysql_passwd,db=settings.mysql_db_test2,port=settings.mysql_port)

def reconnect():
    db.ping(reconnect=True)

#create tables adaptively by the setting file
def create_all_tables():
    for name in mysql_init.table_name: 
        table_init=mysql_init.table_inits[name]
        sql_temp=None
        for key,value in table_init.items():
            if key == "image_name":
                sql_temp=key+" "+value+" "+"PRIMARY KEY"
            else:
                sql_temp=",".join([sql_temp,(key+" "+value+" "+"NOT NULL")])
        sql_temp="create TABLE IF NOT EXISTS "+name+"("+sql_temp+")DEFAULT CHARACTER SET utf8;"
        try:
            cursor=db.cursor()
            cursor.execute(sql_temp)
            cursor.close()
        except Exception as e:
            logging.exception(e)

#insert the relative field into the table
def insert_into_table_aoi_image(image_type,param):
    if image_type not in mysql_init.table_name:
        logging.info("The table of"+image_type+"not exists")
    else:
        insert_sql_temp=None
        table_init=mysql_init.table_inits[image_type]
        insert_sql_temp=",".join(list(table_init))
        insert_sql_temp="REPLACE INTO "+image_type+"("+insert_sql_temp+")VALUES("+(",".join(["%s" for i in range(len(table_init.keys()))]))+");"
        try:
            cursor=db.cursor()
            cursor.execute(insert_sql_temp,param)
            db.commit()
            cursor.close()
        except Exception as e:
            logging.exception(e)

#insert the relative field into the table
def insert_into_table_image_new(image_tableName,param):
    insert_sql_temp=None    
    table_fields=",".join(list(mysql_init.Image_Table_Fields_Define_Detection_Segmentation))
    insert_sql_temp="REPLACE INTO "+image_tableName+"("+table_fields+")VALUES("+(",".join(["%s" for i in range(len(mysql_init.Image_Table_Fields_Define_Detection_Segmentation.keys()))]))+");"
    try:
        cursor=db.cursor()
        cursor.execute(insert_sql_temp,param)
        db.commit()
        cursor.close()
    except Exception as e:
        logging.exception(e)
     
#insert the relative field into the table

def insert_into_table_image_v2(image_tableName,task,param,JsonSaveToFile=True):
    if task in ["Detection","Segmentation"]:
        if JsonSaveToFile:
            insert_sql_temp=None    
            table_fields=",".join(list(mysql_init.Image_Table_Fields_Define_Detection_Segmentation_jsonFile))
            insert_sql_temp="REPLACE INTO "+image_tableName+"("+table_fields+")VALUES("+(",".join(["%s" for i in range(len(mysql_init.Image_Table_Fields_Define_Detection_Segmentation_jsonFile.keys()))]))+");"
            
            param_new=(param["Uuid"],param["MachineId"],param["ProjectName"],
            param["ProductName"],param["BarCode"],param["ImageName"],
            param["LabelType"],param["LabelsPath"],param["GenerateDateTime"])
            
            try:
                #save json to files
                with open(param["LabelsPath"],'w') as of:
                    json.dump(param["Labels"],of)
              
                cursor=db.cursor()
                cursor.execute(insert_sql_temp,param_new)
                db.commit()
                cursor.close()
            except Exception as e:
                logging.exception(e)
        else:
            insert_sql_temp=None    
            table_fields=",".join(list(mysql_init.Image_Table_Fields_Define_Detection_Segmentation))
            insert_sql_temp="REPLACE INTO "+image_tableName+"("+table_fields+")VALUES("+(",".join(["%s" for i in range(len(mysql_init.Image_Table_Fields_Define_Detection_Segmentation.keys()))]))+");"
            
            
            param_new=(param["Uuid"],param["MachineId"],param["ProjectName"],
            param["ProductName"],param["BarCode"],param["ImageName"],
            param["LabelType"],param["Labels"],param["GenerateDateTime"])            
            try:
                cursor=db.cursor()
                cursor.execute(insert_sql_temp,param_new)
                db.commit()
                cursor.close()
            except Exception as e:
                logging.exception(e)
    elif task in ["Classification"]:
        insert_sql_temp=None    
        table_fields=",".join(list(mysql_init.Image_Table_Fields_Define_Classification))
        insert_sql_temp="REPLACE INTO "+image_tableName+"("+table_fields+")VALUES("+(",".join(["%s" for i in range(len(mysql_init.Image_Table_Fields_Define_Classification.keys()))]))+");"
        
        param_new=(param["Uuid"],param["MachineId"],param["ProjectName"],
        param["ProductName"],param["BarCode"],param["ImageName"],
        param["LabelType"],param["ObjectType"],param["ObjectName"],
        param["label"],param["GenerateDateTime"])   
        
        try:
            cursor=db.cursor()
            cursor.execute(insert_sql_temp,param_new)
            db.commit()
            cursor.close()
        except Exception as e:
            logging.exception(e)
    else:
        print("task ",task," is not in Classification,Detection,Segmentation")
    

#insert manydata into table      
def insertmany_into_table_aoi_image(image_type,params):
    if image_type not in mysql_init.table_name:
        logging.info("The table of"+image_type+"not exists")
    else:
        insert_sql_temp=None
        table_init=mysql_init.table_inits[image_type]
        insert_sql_temp=",".join(list(table_init))
        insert_sql_temp="REPLACE INTO "+image_type+"("+insert_sql_temp+")VALUES("+(",".join(["%s" for i in range(len(table_init.keys()))]))+");"
        try:
            cursor=db.cursor()
            cursor.execute(insert_sql_temp,params)
            db.commit()
            cursor.close()
        except Exception as e:
            logging.exception(e)

#select name by product,component(产品（单板），器件类型（SC0402）)
def execute_select_all_by_type(image_type,product_type,device_type):
    if image_type not in mysql_init.table_name:
        logging.info("The table of"+image_type+"not exists")
    else:
        query_sql_temp=None
        query_sql_temp="SELECT image_name FROM "+image_type+" WHERE product_type='{}' AND component='{}';"
        try:
            cursor=db.cursor()
            cursor.execute(query_sql_temp.format(product_type,device_type))
            data=cursor.fetchall()
            db.commit()
            cursor.close()
            return data
        except Exception as e:
            logging.exception(e)

#select name by product,component，label(产品（单板），器件类型（SC0402）,标签（正）)
def execute_select_all_by_defection_type(image_type,product_type,device_type,label):
    if image_type not in mysql_init.table_name:
        logging.info("The table of"+image_type+"not exists")
    else:
        query_sql_temp=None
        query_sql_temp="SELECT image_name FROM "+image_type+" WHERE product_type='{}' AND component='{}' AND label='{}';"
        try:
            cursor=db.cursor()
            cursor.execute(query_sql_temp.format(product_type,device_type,label))
            data=cursor.fetchall()
            db.commit()
            cursor.close()
            return data
        except Exception as e:
            logging.exception(e)

#select name by product,component，label，time_point(产品（单板），器件类型（SC0402）,标签（正）,产生时间（‘20181120’）)
def execute_select_all_by_time(image_type,product_type,device_type,label,time_point):
    if image_type not in mysql_init.table_name:
        logging.info("The table of"+image_type+"not exists")
    else:
        query_sql_temp=None
        query_sql_temp="SELECT image_name FROM "+image_type+" WHERE product_type='{}' AND component='{}' AND label='{}' AND DATE_FORMAT(time_point,'%Y%m%d')='{}';"
        try:
            cursor=db.cursor()
            cursor.execute(query_sql_temp.format(product_type,device_type,label,time_point))
            data=cursor.fetchall()
            db.commit()
            cursor.close()
            return data
        except Exception as e:
            logging.exception(e)

def Find_Items(table_name,field):
    if table_name not in mysql_init.table_name:
        logging.info("The table of"+image_type+"not exists")
    else:
        query_sql_temp=None
        query_sql_temp="SELECT DISTINCT "+field+" FROM "+table_name
        try:
            cursor=db.cursor()
            cursor.execute(query_sql_temp)
            Items=cursor.fetchall()
            db.commit()
            cursor.close()
            return Items
        except Exception as e:
            logging.exception(e)

# def Find_imagenames(table_name,field_option):
#     if table_name not in mysql_init.table_name:
#         logging.info("The table of"+image_type+"not exists")
#     else:
#         query_sql_temp="SELECT image_name From "+table_name+" WHERE "
#         for key,value in field_option.items():
#             if value=='ALL':
#                 continue
#             if key=='time_point':
#                 query_sql_temp=query_sql_temp+"DATE_FORMAT(time_point,'%Y%m%d')>="+"'"+value[0]+"'"+" AND "+"DATE_FORMAT(time_point,'%Y%m%d')<="+"'"+value[1]+"'"
#             else:
#                 query_sql_temp=query_sql_temp+key+"="+"'"+value+"'"+" AND "
#         print (query_sql_temp)
#         try:
#             cursor=db.cursor()
#             cursor.execute(query_sql_temp)
#             images=cursor.fetchall()
#             db.commit()
#             cursor.close()
#             return images
#         except Exception as e:
#             logging.exception(e)
def Find_imagenames(table_name,field_option):
    if table_name not in mysql_init.table_name:
        logging.info("The table of"+image_type+"not exists")
    else:
        query_sql_temp="SELECT image_name From "+table_name+" WHERE "
        for key,values in field_option.items():
            if values[0]=='ALL':
                continue
            if key=='time_point':
                query_sql_temp=query_sql_temp+"DATE_FORMAT(time_point,'%Y%m%d')>="+"'"+values[0]+"'"+" AND "+"DATE_FORMAT(time_point,'%Y%m%d')<="+"'"+values[1]+"'"
            else:
                query_sql_temp=query_sql_temp+key+" in "+"("
                for value in values:
                    query_sql_temp=query_sql_temp+"'"+value+"',"
                query_sql_temp=query_sql_temp[:-1]
                query_sql_temp=query_sql_temp+") AND "
        print (query_sql_temp)
        try:
            cursor=db.cursor()
            cursor.execute(query_sql_temp)
            images=cursor.fetchall()
            db.commit()
            cursor.close()
            return images
        except Exception as e:
            logging.exception(e)


def init():
    create_all_tables()







#4.复制旧表的数据到新表(假设两个表结构不一样) 
#INSERT INTO 新表(字段1,字段2,.......) SELECT 字段1,字段2,...... FROM 旧表

# table_inits={"BoardAOI":{"image_name":"VARCHAR(100)",
#                         "device_id":"VARCHAR(20)",
#                         "time_point":"DATETIME",
#                         "product_type":"VARCHAR(20)",
#                         "board_id":"VARCHAR(20)",
#                         "component":"VARCHAR(20)",
#                         "board_loc":"VARCHAR(20)",
#                         "label":"VARCHAR(5)"
#                         },
#             "WirelessAOI":{"image_name":"VARCHAR(80)",
#                         "board_id":"VARCHAR(30)",
#                         "mission_id":"VARCHAR(30)",
#                         "time_point":"DATETIME",
#                         "label":"VARCHAR(5)"
#                         }
#             }
def alter_old_to_new_mysql_table(original_BoardAOI_table,new_table_name):
    # insert_sql_temp=None
    # table_init=mysql_init.table_inits[image_type]
    # insert_sql_temp=",".join(list(table_init))
    # insert_sql_temp="REPLACE INTO "+image_type+"("+insert_sql_temp+")VALUES("+(",".join(["%s" for i in range(len(table_init.keys()))]))+");"
    #UUID=uuid.uuid1()

    insert_sql_temp='''
    INSERT INTO '''+new_table_name+'''(
       Uuid,ImageName,GenerateDateTime   
       ) 
    SELECT Uuid_id,image_name,time_point 
    FROM '''+original_BoardAOI_table
    try:
        cursor=db.cursor()
        cursor.execute(insert_sql_temp)
        db.commit()
        cursor.close()
    except Exception as e:
        logging.exception(e)


#{"MachineId":"HWJC20190424001",
# "ProjectName":"单板器件外观检测",
# "ProductName":"03023-PFK",
# "BarCode":"2102312CEX10K4011991",
# "ImageName":"logo001.jpg",
# "ImageRawData":null,
# "LabelType":"分类",
# "Labels":
#       [{"ObjectName":"R1534",
#       "ROIType":"整图",
#       "ROIPoints":[{"X":0,"Y":0},{"X":200,"Y":160}],
#       "ObjectType":"HD-SFLT4-0101",
#       "Label":"OK"}],
#"GenerateDateTime":"2019-04-28 20:18:58"}
def create_new_table_by_type(new_table_name):
    # creat_sql='''CREATE TABLE IF NOT EXISTS '''+new_table_name+'''(
    #     Uuid VARCHAR(36) PRIMARY KEY NOT NULL,
    #     MachineId VARCHAR(100),
    #     ProjectName VARCHAR(100),
    #     ProductName VARCHAR(100),
    #     BarCode VARCHAR(100),
    #     ImageName VARCHAR(200) NOT NULL,
    #     LabelType VARCHAR(100),
    #     Labels VARCHAR(500),
    #     GenerateDateTime DATETIME)
    #     DEFAULT CHARACTER SET utf8;'''

    sql_temp=""
    for k,v in mysql_init.Image_Table_Fields_Define_Detection_Segmentation.items():
        if k=="Uuid":#primary key
            sql_temp=k+" "+v+" "+"PRIMARY KEY"
        elif k in ["ImageName"]:#not null
             sql_temp=",".join([sql_temp,(k+" "+v+" "+"NOT NULL")])
        else:
            sql_temp=",".join([sql_temp,(k+" "+v)])
    sql_temp="create TABLE IF NOT EXISTS "+new_table_name+"("+sql_temp+")DEFAULT CHARACTER SET utf8;"

    try:
        cursor=db.cursor()
        cursor.execute(sql_temp)#.format(new_table_name))#creat_sql.format(new_table_name)
        cursor.close()
    except Exception as e:
        logging.exception(e)

def create_new_table_by_type_task(new_table_name,task,JsonSaveToFile=True):
    # creat_sql='''CREATE TABLE IF NOT EXISTS '''+new_table_name+'''(
    #     Uuid VARCHAR(36) PRIMARY KEY NOT NULL,
    #     MachineId VARCHAR(100),
    #     ProjectName VARCHAR(100),
    #     ProductName VARCHAR(100),
    #     BarCode VARCHAR(100),
    #     ImageName VARCHAR(200) NOT NULL,
    #     LabelType VARCHAR(100),
    #     Labels VARCHAR(500),
    #     GenerateDateTime DATETIME)
    #     DEFAULT CHARACTER SET utf8;'''
    if task in ["Detection","Segmentation"]:
        if JsonSaveToFile:
            #new_table_name=new_table_name+"_Detection_Segmentation"
            sql_temp=""
            for k,v in mysql_init.Image_Table_Fields_Define_Detection_Segmentation_jsonFile.items():
                if k=="Uuid":#primary key
                    sql_temp=k+" "+v+" "+"PRIMARY KEY"
                elif k in ["ImageName"]:#not null
                    sql_temp=",".join([sql_temp,(k+" "+v+" "+"NOT NULL")])
                else:
                    sql_temp=",".join([sql_temp,(k+" "+v)])
            sql_temp="create TABLE IF NOT EXISTS "+new_table_name+"("+sql_temp+")DEFAULT CHARACTER SET utf8;"

            try:
                cursor=db.cursor()
                cursor.execute(sql_temp)#.format(new_table_name))#creat_sql.format(new_table_name)
                cursor.close()
            except Exception as e:
                logging.exception(e)

            #pass
        else:
            #new_table_name=new_table_name+"_Detection_Segmentation_withjson"
            sql_temp=""
            for k,v in mysql_init.Image_Table_Fields_Define_Detection_Segmentation.items():
                if k=="Uuid":#primary key
                    sql_temp=k+" "+v+" "+"PRIMARY KEY"
                elif k in ["ImageName"]:#not null
                    sql_temp=",".join([sql_temp,(k+" "+v+" "+"NOT NULL")])
                else:
                    sql_temp=",".join([sql_temp,(k+" "+v)])
            sql_temp="create TABLE IF NOT EXISTS "+new_table_name+"("+sql_temp+")DEFAULT CHARACTER SET utf8;"

            try:
                cursor=db.cursor()
                cursor.execute(sql_temp)#.format(new_table_name))#creat_sql.format(new_table_name)
                cursor.close()
                return new_table_name
            except Exception as e:                
                logging.exception(e)
               
    elif task in ["Classification"]:
        #new_table_name=new_table_name+"_Classification"
        sql_temp=""
        for k,v in mysql_init.Image_Table_Fields_Define_Classification.items():
            if k=="Uuid":#primary key
                sql_temp=k+" "+v+" "+"PRIMARY KEY"
            elif k in ["ImageName"]:#not null
                sql_temp=",".join([sql_temp,(k+" "+v+" "+"NOT NULL")])
            else:
                sql_temp=",".join([sql_temp,(k+" "+v)])
        sql_temp="create TABLE IF NOT EXISTS "+new_table_name+"("+sql_temp+")DEFAULT CHARACTER SET utf8;"

        try:
            cursor=db.cursor()
            cursor.execute(sql_temp)#.format(new_table_name))#creat_sql.format(new_table_name)
            cursor.close()
            return new_table_name
        except Exception as e:
            logging.exception(e)           
    else:
        print("no create data table")
        print("task ",task," is not in Classification,Detection,Segmentation")
        #return None

# insert_into_table_aoi_image()
# execute_select_all_by_type()
if __name__=="__main__":
    #init()
    
    print("###"*20,"start mysql","###"*10)
    #alter_old_to_new_mysql_table("BoardAOI_temp","newImageTable")
    UUID=uuid.uuid5(uuid.NAMESPACE_DNS,"None")
    print("type(UUID)",type(UUID))

    lables_json='{\"ObjectName\":\"R1534\",\"ROIType\":\"wholepic\",\"ROIPoints\":\"path/to/roipoints\",\"ObjectType\":\"HD-SFLT4-0101\",\"Label\": \"OK\"}'
    lables_json2='{\"ObjectName\":\"R1234\",\"ROIType\":\"smallpic\",\"ROIPoints\":\"path/to/roipoints2\",\"ObjectType\":\"HD-SFLT4-0102\",\"Label\": \"NO\"}'
    insert_sql='['+lables_json+','+lables_json2+']'
    print("mysql json:",insert_sql)
    dict_test={
        "Uuid":str(UUID),
        "MachineId":"HWJC20190424001",
        "ProjectName":"board_test2",
        "ProductName":"03023-PFK",
        "BarCode":"2102312CEX10K4011991",
        "ImageName":"logo001.jpg",
        "ImageRawData":"None",
        "LabelType":"class",
        "Labels":insert_sql,
        
        # '''[{"ObjectName":"R1534",
        # "ROIType":"整图",
        # "ROIPoints":[{"X":0,"Y":0},{"X":200,"Y":160}],
        # "ObjectType":"HD-SFLT4-0101",
        # "Label":"OK"}]''',
        "GenerateDateTime":"2019-04-28 20:18:58"
    }
    insert_data=(dict_test["Uuid"],dict_test["MachineId"],
    dict_test["ProjectName"],dict_test["ProductName"],
    dict_test["BarCode"],dict_test["ImageName"],
    dict_test["LabelType"],dict_test["Labels"],
    dict_test["GenerateDateTime"])
    











    #create_new_table_by_type(dict_test['ProjectName'])
    #CurrtableName=create_new_table_by_type_task(dict_test['ProjectName'],dict_test["LabelType"])
    testtype=["Classification","Detection","Segmentation"]
    ProjectNametest=["project1","project2"]
    for i in range(10):

        dict_test["ImageName"]=str(i+60)+".bmp"
        #print(dict_test["ImageName"])

        #URL,OID...
        UUID=uuid.uuid5(uuid.NAMESPACE_DNS, str(i)+dict_test["ImageName"])
        dict_test["Uuid"]=str(UUID)
        dict_test["ProjectName"]=ProjectNametest[i%2]
        dict_test["LabelType"]=testtype[i%3]
        dict_test["BarCode"]=None if i%2 else "1234321"#"NULL"


        insert_data=(dict_test["Uuid"],dict_test["MachineId"],
        dict_test["ProjectName"],dict_test["ProductName"],
        dict_test["BarCode"],dict_test["ImageName"],
        dict_test["LabelType"],dict_test["Labels"],
        dict_test["GenerateDateTime"])
        

        #如何解析出ObjectType，ObjectName，label

        curr_obj_type="curr_obj_type"
        curr_obj_name="curr_obj_name"
        curr_label="curr_label"
        curr_labels_path=dict_test["ImageName"]

        CurrParamDict={}
        CurrParamDict.update({"Uuid":dict_test["Uuid"]})
        CurrParamDict.update({"MachineId":dict_test["MachineId"]})
        CurrParamDict.update({"ProjectName": dict_test["ProjectName"]})
        CurrParamDict.update({"ProductName":dict_test["ProductName"]})
        CurrParamDict.update({"BarCode": dict_test["BarCode"]})
        CurrParamDict.update({"ImageName":dict_test["ImageName"]})
        CurrParamDict.update({"LabelType":dict_test["LabelType"]})
        CurrParamDict.update({"Labels":dict_test["Labels"]})
        CurrParamDict.update({"GenerateDateTime":dict_test["GenerateDateTime"]})
        CurrParamDict.update({"ObjectType":curr_obj_type})
        CurrParamDict.update({"ObjectName":curr_obj_name})
        CurrParamDict.update({"label":curr_label})
        CurrParamDict.update({"LabelsPath":curr_labels_path})

        jsonsavetofile=True
        CurrtableName=None
        if dict_test["LabelType"] in ["Detection","Segmentation"] and jsonsavetofile:
            CurrtableName=dict_test['ProjectName']+"_Detection_Segmentation"
        elif dict_test["LabelType"] in ["Detection","Segmentation"] and not jsonsavetofile:
            CurrtableName=dict_test['ProjectName']+"_Detection_Segmentation_withjson"
        elif dict_test["LabelType"] in ["Classification"]:
            CurrtableName=dict_test['ProjectName']+"_Classification"
        else:
            CurrtableName=None


        
        
        

        create_new_table_by_type_task(dict_test['ProjectName'],dict_test["LabelType"])
        #print("currenttable Name:",i,CurrtableName)
        if CurrtableName:
        #insert_into_table_image_new(dict_test['ProjectName'],insert_data)
            insert_into_table_image_v2(CurrtableName,dict_test["LabelType"],CurrParamDict)
            print(i,"insert "+dict_test["ImageName"]+" into "+"table "+CurrtableName)
    print("###"*20,"end mysql","###"*10)