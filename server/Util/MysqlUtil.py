import sys
sys.path.append("../configs")
sys.path.append("configs")
import settings
import pymysql
import logging
import datetime

# db=pymysql.connect(host=settings.mysql_host,user=settings.mysql_user,password=settings.mysql_passwd,db=settings.mysql_db,port=settings.mysql_port)
db=pymysql.connect(host=settings.mysql_host,user=settings.mysql_user,password=settings.mysql_passwd,db=settings.mysql_db_test,port=settings.mysql_port)
CREATE_TABLE_IMAGE_AOI='''
create TABLE IF NOT EXISTS aoi_image(
    image_name VARCHAR(100) PRIMARY KEY,
    product_type VARCHAR(50) NOT NULL,
    device_type VARCHAR(50) NOT NULL,
    label VARCHAR(5) NOT NULL,
    board_id VARCHAR(20) NOT NULL,
    board_loc VARCHAR(20) NOT NULL,
    time_point DATETIME NOT NULL
)DEFAULT CHARACTER SET utf8;
'''

INSERT_INTO_TABLE_IMAGE_AOI='''
REPLACE INTO aoi_image(
    image_name,
    product_type,
    device_type,
    label,
    board_id,
    board_loc,
    time_point
)VALUES(
    %s,%s,%s,%s,%s,%s,%s
);
'''

SELECT_FROM_AOI_IMAGE_BY_TYPE='''
SELECT
    image_name
FROM aoi_image WHERE product_type='{}' AND device_type='{}'
'''

SELECT_FROM_AOI_IMAGE_BY_DEFECTION_TYPE='''
SELECT
    image_name
FROM aoi_image WHERE product_type='{}' AND device_type='{}' AND label='{}'
'''

SELECT_FROM_AOI_IMAGE_BY_TIME='''
SELECT
    image_name
FROM aoi_image WHERE product_type='{}' AND device_type='{}' AND label='{}' AND DATE_FORMAT(time_point,"%Y%m%d")='{}'
'''


def create_table_aoi_image():
    try:
        cursor=db.cursor()
        cursor.execute(CREATE_TABLE_IMAGE_AOI)
        cursor.close()
    except Exception as e:
        logging.exception(e)

def insert_into_table_aoi_image(param):
    try:
        cursor=db.cursor()
        cursor.execute(INSERT_INTO_TABLE_IMAGE_AOI,param)
        db.commit()
        cursor.close()
    except Exception as e:
        logging.exception(e)

def insertmany_into_table_aoi_image(params):
    try:
        cursor=db.cursor()
        cursor.execute(INSERT_INTO_TABLE_IMAGE_AOI,param)
        db.commit()
        cursor.close()
    except Exception as e:
        logging.exception(e)

def execute_select_all_by_type(product_type,device_type):
    try:
        cursor=db.cursor()
        cursor.execute(SELECT_FROM_AOI_IMAGE_BY_TYPE.format(product_type,device_type))
        data=cursor.fetchall()
        db.commit()
        cursor.close()
        return data
    except Exception as e:
        logging.exception(e)

def execute_select_all_by_defection_type(product_type,device_type,label):
    try:
        cursor=db.cursor()
        cursor.execute(SELECT_FROM_AOI_IMAGE_BY_DEFECTION_TYPE.format(product_type,device_type,label))
        data=cursor.fetchall()
        db.commit()
        cursor.close()
        return data
    except Exception as e:
        logging.exception(e)

def execute_select_all_by_time(product_type,device_type,label,time_point):
    try:
        cursor=db.cursor()
        cursor.execute(SELECT_FROM_AOI_IMAGE_BY_TIME.format(product_type,device_type,label,time_point))
        data=cursor.fetchall()
        db.commit()
        cursor.close()
        return data
    except Exception as e:
        logging.exception(e)



def init():
    create_table_aoi_image()

if __name__=="__main__":
    init()
    # insert_data=("0_0_180328161718_OK_3.bmp","CAE_train_image4","0","B20181218","L12345","2017-11-19 18:24:46")
    # insert_into_table_aoi_image(insert_data)
    # time_now=datetime.datetime.now()
    # print (time_now)
    # print (time_now.date())
    # print (time_now.time())
    # print (time_now.strftime('%Y-%m-%d %H:%M:%S'))
    # print (type(time_now.strftime('%Y-%m-%d %H:%M:%S')))
    # query_aoi_type='CAE_train_image4'
    # query_defection_type='0'
    # query_time_point='20171019'
    # aoi_results = execute_select_all_by_type(query_aoi_type)
    # aoi_results=execute_select_all_by_defection_type(query_aoi_type,query_defection_type)
    # aoi_results=execute_select_all_by_time(query_aoi_type,query_defection_type,query_time_point)
    # print (aoi_results)

