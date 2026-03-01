from shared.kafka.producer import KafkaProducer
from process_files import OpenFiles
from logging import Logger 
import os 

class ServiceManager():
    def __init__(self,producer: KafkaProducer, open_files : OpenFiles, logger : Logger):
        self.logger = logger 
        self.producer = producer
        self.open_files = open_files
        
    def handle_file(self, file:str):
        try:
            event = self.open_files.get_file_metadata(file)
            self.producer.send_event(event)
        except Exception:
            self.logger.error("error",exc_info=True)
            raise
        
    def run(self):
        try:
            for file in os.listdir(self.open_files.path_to_dir):
                self.handle_file(file)        
        except Exception:
            self.logger.error("error in running",exc_info=True)
            raise

