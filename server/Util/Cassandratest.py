import sys
import os
import io
sys.path.append("../configs")
sys.path.append("configs")
import settings
import logging
from cassandra.cluster import Cluster

#connect to the cassandra server
cluster=Cluster(["127.0.0.1"])
session=cluster.connect("imagekeyspace_test2")

CREATE_IMAGE_TABLE='''
CREATE TABLE image_table(image_name varchar PRIMARY KEY,
    image_data blob);
'''

INSERT_INTO_IMAGE_TABLE='''
INSERT INTO image_table(image_name,image_data) VALUES (
    %s,%s
);
'''

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

def init():
    create_image_table()

if __name__=="__main__":
    file_name1="HWJC20190123001_20190201115744916_025DFK_025DFK186C013782_HSC0402-HDTD_L5929_NG.bmp"
    file_name2="HWJC20190123001_20190201115803723_025DFK_025DFK186C013782_SMD3-34_J5915_OK.bmp"
    image_data=bytearray(open(file_name2,'rb').read())
    insert_into_image_table(file_name2,image_data)
    # init()