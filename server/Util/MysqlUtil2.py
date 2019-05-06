import sys
sys.path.append("../configs")
sys.path.append("configs")
import settings
import mysql_init
import pymysql
import logging
import datetime

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




def try_create_the_tables(image_type_table_name):
    
    sql_temp=None
    sql_temp='''
    create TABLE IF NOT EXISTS %s(
    image_name VARCHAR(100) PRIMARY KEY,
    product_type VARCHAR(50) NOT NULL,
    device_type VARCHAR(50) NOT NULL,
    label VARCHAR(5) NOT NULL,
    board_id VARCHAR(20) NOT NULL,
    board_loc VARCHAR(20) NOT NULL,
    time_point DATETIME NOT NULL
    )DEFAULT CHARACTER SET utf8;
    '''


    try:
        cursor=db.cursor()
        cursor.execute(sql_temp,image_type_table_name)
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

# insert_into_table_aoi_image()
# execute_select_all_by_type()
if __name__=="__main__":
    init()