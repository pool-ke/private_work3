import sys
sys.path.append("../configs")
sys.path.append("configs")
import settings

import happybase
import json
import logging

# pool=happybase.ConnectionPool(size=settings.hbase_pool_size,host=settings.hbase_host,table_prefix=settings.hbase_table_prefix,protocol='compact')
pool=happybase.ConnectionPool(size=settings.hbase_pool_size,host=settings.hbase_host)
# pool=happybase.ConnectionPool(size=3,host='127.0.0.1')

def create_table(table_name):
    try:

        with pool.connection() as conn:
            conn.create_table(table_name,{'index':dict(max_versions=1),'data':dict(max_versions=1)})
    except Exception as e:
        logging.exception(e)
        return False
    return True

def put_index(dictData):
    try:
        with pool.connection() as conn:
            table=conn.table(settings.hbase_table_name)
            with table.batch(batch_size=20) as b:
                for(key,value) in dictData.items():
                    data={'index:mapfileid':value}
                    imageId=key
                    b.put(imageId,data)
    except Exception as e:
        logging.exception(e)
        return False
    return True
def put_data(dictData):
    try:
        with pool.connection() as conn:
            table=conn.table(settings.hbase_table_name)
            #imageIds=dictData.keys()
            #mapfileId=dictData.values()[0]
            imageIds=list(dictData.keys())
            mapfileId=list(dictData.values())[0]
            table.put(mapfileId,{'data:imageIds':json.dumps(imageIds)})
    except Exception as e:
        logging.exception(e)
        return False
    return True

def put(data):
    return put_index(data) and put_data(data)

def getImageIds(mapFileId):
    try:
        with pool.connection() as conn:
            table=conn.table(settings.hbase_table_name)
            row=table.row(mapFileId)
            print (row)
            imageIds=json.loads(row[b'data:imageIds'])
            # imageIds=json.loads(row[('data:imageIds').encode('utf-8')])
    except Exception as e:
        logging.exception(e)
        imageIds=None
    return imageIds

def getMapFileId(imageId):
    try:
        with pool.connection() as conn:
            table=conn.table(settings.hbase_table_name)
            imageId=imageId.encode("utf-8")
            row=table.row(imageId)
            logging.info(row)
            mapfileId=row[b'index:mapfileid']
            mapfileId=mapfileId.decode('utf-8')
    except Exception as e:
        logging.exception(e)
        mapfileId=None
    return mapfileId

def init():
    create_table(settings.hbase_table_name)

def _test():
    with pool.connection() as conn:
        table=conn.table('image')
        row=table.row('xxxx.jpg')
        print (row)

if __name__ =='__main__':
    init()
    # test_dict={}
    # test_dict['111.jpg']='1'
    # test_dict['222.jpg']='1'
    # test_dict['333.jpg']='1'
    # put_index(test_dict)
    # put_data(test_dict)
    # test_mapFileId='1'
    # print(getImageIds(test_mapFileId))
    # test_imageId='111.jpg'
    # print (getMapFileId(test_imageId))
    # test_imageId='777.jpg'
    # print (getMapFileId(test_imageId))