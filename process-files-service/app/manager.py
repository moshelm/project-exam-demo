from shared.kafka.consumer import KafkaConsumer, KafkaException
from shared.elasticsearch_connection import ElasticConnection
from mongo_stor import StorAudioMongo
from logging import Logger 
import hashlib

class FileProcessor():
    def __init__(self,elastic : ElasticConnection, mongodb : StorAudioMongo, consumer: KafkaConsumer, logger : Logger):
        self.logger = logger 
        self.consumer = consumer
        self.elastic = elastic
        self.mongodb = mongodb

    def generate_id(self,file_metadata:dict):
        try:
            code = f'{file_metadata["file_name"]}_{file_metadata['file_create_date']}'
            return hashlib.md5(code.encode()).hexdigest()
        except Exception:
            self.logger.error("failed generate id",exc_info=True)
            raise
    
    def handle_file(self, value:dict):
        try:
            file_id = self.generate_id(value['metadata'])
            file_name = value['metadata']['file_name']
            self.elastic.insert(value["metadata"],file_id)
            with open(value["file_path"],'br') as file: 
                self.mongodb.insert(file_name,file,file_id)
        except KafkaException:
            self.logger.critical("kafka failed",exc_info=True)
            raise
        except Exception:
            self.logger.error("error",exc_info=True)
            raise
        
    def run(self):
        try:
            self.consumer.run(self.handle_file)    
        except KafkaException:
            self.logger.critical("kafka failed",exc_info=True)
            raise
        except Exception:
            self.logger.error("error in running",exc_info=True)
        

