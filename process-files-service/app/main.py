import logging 
from manager import ServiceManager
from process_files import OpenFiles
from service_config import ServiceConfig
from shared.kafka.producer import KafkaProducer

config = ServiceConfig()
config.validate()

logging.basicConfig(
    level=config.level_log,
    format=f'%(asctime)s | {config.service_name} | %(name)s - %(levelname)s -  %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

producer_logger = logging.getLogger("producer")
open_files_logger = logging.getLogger("open_files")
manager_logger = logging.getLogger("manager")

def main():
    try:
        open_files = OpenFiles(config.data_path,open_files_logger)
        producer = KafkaProducer(config.kafka_connect,config.topic,producer_logger)
        manager = ServiceManager(producer,open_files,manager_logger)

        manager.run()

    except Exception:
        raise

if __name__=="__main__":
    main()