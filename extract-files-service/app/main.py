import logging 
from manager import FileProcessor
from process_files import FileMetadata
from service_config import ServiceConfig
from shared.kafka.producer import KafkaProducer, KafkaException
from shared.logger_elastic import Logger

config = ServiceConfig()
config.validate()

logging.getLogger("pymongo").setLevel(logging.ERROR)
logging.getLogger("elasticsearch").setLevel(logging.ERROR)
logging.getLogger("confluent_kafka").setLevel(logging.ERROR)

logger = Logger.get_logger(config.service_name, config.elastic_config, config.index_logger)

# logging.basicConfig(
#     level=config.level_log,
#     format=f'%(asctime)s | {config.service_name} | %(name)s - %(levelname)s -  %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S'
# )

# producer_logger = logging.getLogger("producer")
# file_processor_logger = logging.getLogger("file_processor")
# manager_logger = logging.getLogger("manager")


def main():
    try:
        file_processor = FileMetadata(config.data_path,logger)
        producer = KafkaProducer(config.kafka_connect,config.topic,logger)
        manager = FileProcessor(producer,file_processor,logger)

        manager.run()
    except KafkaException:
        raise
    except Exception:
        raise
    finally:
        producer.close()

if __name__=="__main__":
    try:
        main()
    except Exception:
        raise