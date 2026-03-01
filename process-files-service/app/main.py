import logging 
from manager import FileProcessor
from process_files import FileMetadata
from service_config import ServiceConfig
from shared.kafka.producer import KafkaProducer, KafkaException

config = ServiceConfig()
config.validate()

logging.basicConfig(
    level=config.level_log,
    format=f'%(asctime)s | {config.service_name} | %(name)s - %(levelname)s -  %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

producer_logger = logging.getLogger("producer")
file_processor_logger = logging.getLogger("file_processor")
manager_logger = logging.getLogger("manager")

def main():
    try:
        file_processor = FileMetadata(config.data_path,file_processor_logger)
        producer = KafkaProducer(config.kafka_connect,config.topic,producer_logger)
        manager = FileProcessor(producer,file_processor,manager_logger)

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