from pykafka import KafkaClient
import logging
from pykafka.protocol import PartitionOffsetFetchRequest

client=KafkaClient(hosts="127.0.0.1:9092")

# print (client.topics)

topic=client.topics['test']
# with topic.get_producer() as producer:
#     for i in range(4):
#         producer.produce(('test message'+str(i**2)).encode('utf-8'))

consumer=topic.get_simple_consumer()
consumer=topic.get_balanced_consumer(
    consumer_group="test",
    zookeeper_connect="127.0.0.1:2181"
)
# consumer.consume()
# consumer.commit_offsets()
for message in consumer:
    if message is not None:
        print (message.offset,message.value)



# offsets=topic.latest_available_offsets()
# print ("The information is follow:")
# for partition,item in offsets.items():
#     print ('partition={},offset={}'.format(partition,item.offset[0]))

# partitions=offsets.keys()
# print ("The information readed is follow:")
# offset_manager=client.cluster.get_offset_manager(('balance-consumer').encode('utf8'))
# requests=[PartitionOffsetFetchRequest((topic_name='test',partition_id=part_id).encode('utf8')) for part_id in partitions]
# response=offset_manager.fetch_consumer_group_offsets('test',requests)

# for partition,item in response.topics['test'].items():
#     print ('partition={},offset={}'.format(partition,item.offset[0]))



