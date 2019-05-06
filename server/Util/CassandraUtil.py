import sys
import os
import io
sys.path.append("../configs")
sys.path.append("configs")
import settings
import logging
from cassandra.cluster import Cluster

#connect to the cassandra server
cluster=Cluster([settings.cassandra_host])
session=cluster.connect(settings.cassandra_keyspace_test)

#create the keyspace
CREATE_KEY_SPACE='''
CREATE KEYSPACE %s WITH REPLICATION={'class':'SimpleStrategy','replication_factor':1}
'''

#create the table in keyspace
CREATE_IMAGE_TABLE='''
CREATE TABLE image_table(image_name varchar PRIMARY KEY,
    image_data blob);
'''

#insert the image data in table(name,data)
INSERT_INTO_IMAGE_TABLE='''
INSERT INTO image_table(image_name,image_data) VALUES (
    %s,%s
);
'''
#select image data from table
SELECT_FROM_IMAGE_NAME='''
SELECT image_data FROM image_table WHERE image_name ='{}'; 
'''
#delete image data from table
DELETE_FROM_IMAGE_NAME='''
DELETE FROM image_table WHERE image_name = '{}';
'''
def create_keyspace(name_keyspace):
    try:
        session.execute(CREATE_KEY_SPACE,name_keyspace)
    except Exception as e:
        logging.exception(e)

def create_image_table():
    try:
        session.execute(CREATE_IMAGE_TABLE)
    except Exception as e:
        logging.exception(e)

def insert_into_image_table(image_name,image_data):
    try:
        session.execute(INSERT_INTO_IMAGE_TABLE,(image_name,image_data))
    except Exception as e:
        logging.exception(e)

def select_by_image_name(image_name):
    try:
        results=session.execute(SELECT_FROM_IMAGE_NAME.format(image_name))
        # return io.BytesIO(results[0][0])
        return results[0][0]
    except Exception as e:
        logging.exception(e)

def delete_from_image_name(image_name):
    try:
        session.execute(DELETE_FROM_IMAGE_NAME.format(image_name))
    except Exception as e:
        logging.exception(e)

def init():
    # create_keyspace(settings.cassandra_keyspace)
    create_image_table()




# rows=session.execute('select * from t_user')
# for row in rows:
#     # print (str(row[0])+str(row[1])+str(row[2]))
#     print (row)


if __name__=="__main__":

    init()
    # image_path='111.bmp'
    # image_data=None
    # with open(image_path,'rb') as f:
    #     image_data=bytearray(f.read())
    #     # print (type(image_data))
    # insert_into_image_table(image_path,image_data)
    

    # save_dir="/home/huawei/image_server/dir_test"
    # save_path=os.path.join(save_dir,'1111.bmp')
    # result=select_by_image_name('111.bmp')
    # if result is not None:
    #     print (1111)
    #     with open(save_path,'wb') as f:
    #         f.write(result)
    

    # result=select_by_image_name('key1')
    # print (result)