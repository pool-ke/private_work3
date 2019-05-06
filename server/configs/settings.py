#image folder path
prepare_dir="/home/huawei/data/kemuyuan/image_server/images/preImages"
queue_dir="/home/huawei/data/kemuyuan/image_server/images/queueImages"
query_dir="/home/huawei/data/kemuyuan/image_server/images/queryImages"
query_dir2="/home/huawei/data/kemuyuan/image_server/images/queryImages2"
dstfile_dir="/home/huawei/data/kemuyuan/image_server/images"


images_cache_folder="/home/huawei/data/kemuyuan/image_server/caches/images"
# mapfile_cache_folder="/home/huawei/image_server/caches/mapfiles"
project_path="/home/huawei/data/kemuyuan/image_server"

mysql_json_file_dir="/home/huawei/data/kemuyuan/image_server/images/JsonOfLabel"

#scp config(only support linux file-system)
server_host="127.0.0.1"
ssh2_port=22
ssh2_username="huawei"
ssh2_passwd="Huawei1234"

#redis config
redis_host="127.0.0.1"
redis_port=6379
redis_db=0

# #HBase config
# hbase_host="127.0.0.1"
# hbase_port=16010
# hbase_table_prefix="v1"
# hbase_table_name="hb_image"
# hbase_pool_size=10
# hbase_time_out=None

#Mysql config
mysql_host="127.0.0.1"
mysql_port=3306
mysql_user="root"
mysql_passwd="root"
mysql_db="image"
mysql_db_test="image_test"
mysql_db_test2="image_test2"

#Cassandra config
cassandra_host="127.0.0.1"
cassandra_keyspace="imagekeyspace"
cassandra_keyspace_test="imagekeyspace_test"

#flask service api
api_host="0.0.0.0"
api_port=8888
api_debug_flag=False
api_threaded=True

#Byte
# MAX_IMAGE_SIZE=200
MAX_IMAGE_SIZE=50

#time interval
time_interval=0.5
