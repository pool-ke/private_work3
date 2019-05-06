import sys
import os
import io
sys.path.append("../configs")
sys.path.append("configs")
import settings
import logging
import uuid
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
CREATE TABLE image_table_cassrandra(Uuid varchar PRIMARY KEY, ImageName varchar,
    image_data blob);
'''

#create the table in keyspace
CREATE_IMAGE_TABLE_UUID_DATA='''
CREATE TABLE image_table_cassrandra(Uuid varchar PRIMARY KEY,
    image_data blob);
'''

#insert the image data in table(uuid,name,data)
INSERT_INTO_IMAGE_TABLE='''
INSERT INTO image_table_cassrandra(Uuid,ImageName,image_data) VALUES (
    %s,%s,%s
);
'''

#insert the image data in table(uuid,data)
INSERT_INTO_IMAGE_TABLE_uuid_imagedata='''
INSERT INTO image_table_cassrandra(Uuid,image_data) VALUES (
    %s,%s
);
'''

#select image data from table
SELECT_FROM_IMAGE_NAME='''
SELECT image_data FROM image_table_cassrandra WHERE ImageName ='{}'; 
'''

# SELECT_FROM_IMAGE_NAME_getuuid='''
# SELECT Uuid FROM image_table_cassrandra WHERE ImageName ='{}'; 
# '''

#select image data from table
SELECT_FROM_IMAGE_UUID='''
SELECT image_data FROM image_table_cassrandra WHERE UUID ='{}'; 
'''

#delete image data from table
DELETE_FROM_IMAGE_NAME='''
DELETE FROM image_table_cassrandra WHERE ImageName = '{}';
'''

#delete image data from table
DELETE_FROM_IMAGE_UUID='''
DELETE FROM image_table_cassrandra WHERE Uuid = '{}';
'''

#select count from table
SELECT_COUNT_FROM_TABLE='''
SELECT count(*) FROM {};
'''

#select image_name from table
SELECT_NAME_FROM_TABLE='''
SELECT ImageName FROM {};
'''
SELECT_UUID_FROM_TABLE='''
SELECT Uuid FROM {};
'''

def create_keyspace(name_keyspace):
    try:
        session.execute(CREATE_KEY_SPACE,name_keyspace)
    except Exception as e:
        logging.exception(e)

def create_image_table(table_name="image_table_cassrandra"):
    try:
        session.execute(CREATE_IMAGE_TABLE)#.format(table_name))
    except Exception as e:
        logging.exception(e)

def create_image_table_uuid_and_data():
    try:
        session.execute(CREATE_IMAGE_TABLE_UUID_DATA)#.format(table_name))
    except Exception as e:
        logging.exception(e)


# def insert_into_image_table(image_name,image_data):
#     try:
#         session.execute(INSERT_INTO_IMAGE_TABLE,(image_name,image_data))
#     except Exception as e:
#         logging.exception(e)

def insert_into_image_table_withUuid(uuid,image_name,image_data):
    try:
        insert_result=session.execute(INSERT_INTO_IMAGE_TABLE,(uuid,image_name,image_data),timeout=8000)
        return insert_result#may no use
    except Exception as e:
        logging.exception(e)


def insert_into_image_table_Uuid_Imagedata(uuid,image_data):
    try:
        insert_result=session.execute(INSERT_INTO_IMAGE_TABLE_uuid_imagedata,(uuid,image_data),timeout=8000)
        return insert_result#may no use
    except Exception as e:
        logging.exception(e)

def select_by_image_name(image_name):
    try:
        results=session.execute(SELECT_FROM_IMAGE_NAME.format(image_name))
        # return io.BytesIO(results[0][0])
        return results[0][0]
    except Exception as e:
        logging.exception(e)

def select_by_image_uuid(uuid):
    try:
        results=session.execute(SELECT_FROM_IMAGE_UUID.format(uuid))
        # return io.BytesIO(results[0][0])
        return results[0][0]
    except Exception as e:
        logging.exception(e)

def delete_from_image_name(image_name):
    try:
        session.execute(DELETE_FROM_IMAGE_NAME.format(image_name))
    except Exception as e:
        logging.exception(e)

def delete_from_image_uuid(uuid):
    try:
        session.execute(DELETE_FROM_IMAGE_UUID.format(uuid))
    except Exception as e:
        logging.exception(e)


def select_count_from_table(table_name='image_table_cassrandra'):
    try:
        sql_tem=SELECT_COUNT_FROM_TABLE.format(table_name)
        print("SELECT_COUNT_FROM_TABLE.format(table_name):",sql_tem)
        results=session.execute(sql_tem)
        return results[0][0]
    except Exception as e:
        logging.exception(e)


def select_name_from_table(table_name='image_table_cassrandra'):
    try:
        results=session.execute(SELECT_NAME_FROM_TABLE.format(table_name))
        # return io.BytesIO(results[0][0])
        return results
    except Exception as e:
        logging.exception(e)

def select_uuid_from_table(table_name='image_table_cassrandra'):
    try:
        results=session.execute(SELECT_UUID_FROM_TABLE.format(table_name))
        # return io.BytesIO(results[0][0])
        return results
    except Exception as e:
        logging.exception(e)

def init():
    # create_keyspace(settings.cassandra_keyspace)
    #create_image_table("image_table_cassrandra")
    # print("create tables\n")
    # create_image_table_uuid_and_data()
    
    
    print("##########################  start  cassandra ############################")
    testimagepath1="HWJC20190123001_20190201115744916_025DFK_025DFK186C013782_HSC0402-HDTD_L5929_NG.bmp"
    testimagepath2="HWJC20190123001_20190201115803723_025DFK_025DFK186C013782_SMD3-34_J5915_OK.bmp"
    
    
    image_data=bytearray(open(testimagepath1,'rb').read())

    #UUID=uuid.uuid5(uuid.NAMESPACE_DNS, testimagepath1)
    UUID=uuid.uuid1()

    #in_res=insert_into_image_table_withUuid(str(UUID),testimagepath1,image_data)
    print("insert data ")
    in_res=insert_into_image_table_Uuid_Imagedata(str(UUID),image_data)#return no use
    #print("type(in_res)",type(in_res))
    #print(in_res)

    sql_tem="SELECT Uuid FROM image_table_cassrandra WHERE Uuid='"+str(UUID)+"'"
    res=session.execute(sql_tem)
    print("type(res)",type(res))#<class 'cassandra.cluster.ResultSet'>
    print("query result :")
    print(res)
    # for row in res:
    #     print(type(row)) #<class 'cassandra.io.asyncorereactor.Row'>
    #     print(row[0],row[1])

    file_count=select_count_from_table()
    if file_count is None:
        print("count is none")
        print("###########################")
    #image_names=select_name_from_table()
    image_uuid=select_uuid_from_table()

    file_count=int(file_count)
    print ("count is ",file_count)
    file_path="/home/huawei/data/kemuyuan/image_server/images/output_image_dengqifeng"

    if not os.path.exists(file_path):
        os.mkdir(file_path)
    for i in range(file_count):
        #image_name=image_names[i][0]
        curr_image_uuid=image_uuid[i][0]
        save_path=os.path.join(file_path,curr_image_uuid)
        print(curr_image_uuid,"save to ",save_path)
        #image_data=select_by_image_name(image_name)
        image_data=select_by_image_uuid(curr_image_uuid)
        if (image_data is not None):
            with open(save_path,'wb') as tosave:
                tosave.write(image_data)
        else:
            print (curr_image_uuid,"no image data")

    print("#"*20,"end","#"*20)

# rows=session.execute('select * from t_user')
# for row in rows:
#     # print (str(row[0])+str(row[1])+str(row[2]))
#     print (row)


if __name__=="__main__":
    
    print("create tables\n")
    create_image_table_uuid_and_data()
    #init()



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




#  def execute(self, query, parameters=None, timeout=_NOT_SET,    
        


#         If an error is encountered while executing the query, an Exception
#         will be raised.

#         `query` may be a query string or an instance of :class:`cassandra.query.Statement`.

#         `parameters` may be a sequence or dict of parameters to bind.  If a
#         sequence is used, ``%s`` should be used the placeholder for each
#         argument.  If a dict is used, ``%(name)s`` style placeholders must
#         be used.

#         `timeout` should specify a floating-point timeout (in seconds) after
#         which an :exc:`.OperationTimedOut` exception will be raised if the query
#         has not completed.  If not set, the timeout defaults to
#         :attr:`~.Session.default_timeout`.  If set to :const:`None`, there is
#         no timeout. Please see :meth:`.ResponseFuture.result` for details on
#         the scope and effect of this timeout.

#         If `trace` is set to :const:`True`, the query will be sent with tracing enabled.
#         The trace details can be obtained using the returned :class:`.ResultSet` object.

#         `custom_payload` is a :ref:`custom_payload` dict to be passed to the server.
#         If `query` is a Statement with its own custom_payload. The message payload
#         will be a union of the two, with the values specified here taking precedence.

#         `execution_profile` is the execution profile to use for this request. It can be a key to a profile configured
#         via :meth:`Cluster.add_execution_profile` or an instance (from :meth:`Session.execution_profile_clone_update`,
#         for example

#         `paging_state` is an optional paging state, reused from a previous :class:`ResultSet`.
#         """
#         return self.execute_async(query, parameters, trace,    