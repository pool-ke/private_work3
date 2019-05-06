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

#select image_name from table
SELECT_NAME_FROM_TABLE='''
SELECT image_name FROM image_table
'''

#select count from table
SELECT_COUNT_FROM_TABLE='''
SELECT count(*) FROM image_table
'''

#delete image data from table
DELETE_FROM_IMAGE_NAME='''
DELETE FROM image_table WHERE image_name = '{}';
'''

def select_count_from_table():
    try:
        results=session.execute(SELECT_COUNT_FROM_TABLE)
        return results[0][0]
    except Exception as e:
        logging.exception(e)

def select_name_from_table():
    try:
        results=session.execute(SELECT_NAME_FROM_TABLE)
        # return io.BytesIO(results[0][0])
        return results
    except Exception as e:
        logging.exception(e)

def select_by_image_name(image_name):
    try:
        results=session.execute(SELECT_FROM_IMAGE_NAME.format(image_name))
        # return io.BytesIO(results[0][0])
        return results[0][0]
    except Exception as e:
        logging.exception(e)

if __name__=="__main__":
    file_path='/home/huawei/cassandra_data'
    file_count=select_count_from_table()
    image_names=select_name_from_table()
    file_count=int(file_count)
    print (file_count)
    for i in range(file_count):
        image_name=image_names[i][0]
        save_path=os.path.join(file_path,image_name)
        image_data=select_by_image_name(image_name)
        if (image_data is not None):
            open(save_path,'wb').write(image_data)
        else:
            print (image_name)


