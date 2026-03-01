from shared.kafka.producer import KafkaProducer, KafkaException
from process_files import FileMetadata
from logging import Logger 
import os 

class FileProcessor():
    def __init__(self,producer: KafkaProducer, file_metadata : FileMetadata, logger : Logger):
        self.logger = logger 
        self.producer = producer
        self.file_metadata = file_metadata

    def handle_file(self, file:str):
        try:
            event = self.file_metadata.get_file_metadata(file)
            self.producer.send_event(event)
        except KafkaException:
            self.logger.critical("kafka failed",exc_info=True)
            raise
        except Exception:
            self.logger.error("error",exc_info=True)
            raise
        
    def run(self):
        if not self.file_metadata.data_path.exists():
            self.logger.critical("not found the base data",exc_info=True)    
        for file in os.listdir(self.file_metadata.data_path):
            try:
                self.handle_file(file)
            except KafkaException:
                self.logger.critical("kafka failed",exc_info=True)
                raise
            except Exception:
                self.logger.error("error in running",exc_info=True)
            

