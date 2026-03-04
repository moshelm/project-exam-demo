import logging 
from manager import FileProcessor
from mongo_stor import StorAudioMongo
from service_config import ServiceConfig
from shared.kafka.consumer import KafkaConsumer, KafkaException
from shared.mongo_connection import MongoConnection
from shared.elasticsearch_connection import ElasticConnection

config = ServiceConfig()
config.validate()

logging.basicConfig(
    level=config.level_log,
    format=f'%(asctime)s | {config.service_name} | %(name)s - %(levelname)s -  %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

consumer_logger = logging.getLogger("consumer")
file_processor_logger = logging.getLogger("file_processor")
manager_logger = logging.getLogger("manager")
mongo_logger = logging.getLogger("mongodb")
elastic_logger = logging.getLogger("elastic")
mongo_tor_logger = logging.getLogger("stor gridfs")

def main():
    try:
        mongodb = StorAudioMongo(config.mongo_config,config.mongo_db,mongo_logger)
        elastic = ElasticConnection(config.elastic_config,config.index_name,elastic_logger)
        consumer = KafkaConsumer(config.kafka_connect,config.topics,consumer_logger)
        manager = FileProcessor(elastic, mongodb, consumer, manager_logger)

        manager.run()
    
    except KafkaException:
        raise
    except Exception:
        raise

if __name__=="__main__":
    try:
        main()
    except Exception:
        raise