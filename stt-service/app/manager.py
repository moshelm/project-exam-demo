from shared.kafka.consumer import KafkaConsumer, KafkaException
from shared.elasticsearch_connection import ElasticConnection
from shared.mongo_connection import MongoConnection
from logging import Logger 
import gridfs
from stt import stt_file
from io import BytesIO

class Orchestrator():
    def __init__(self,elastic : ElasticConnection, mongodb : MongoConnection, language:str, logger : Logger):
        self.logger = logger 
        self.language = language
        self.elastic = elastic
        self.mongodb = mongodb
  
    def handle_file(self, file):
        try:
            file_name = file.filename
            file_id = file.file_id
            file_bytes =file.read()
            file_for_memory = BytesIO(file_bytes)
            file_text = stt_file(file_for_memory, self.language)
            self.elastic.add_new_filed(file_id,file_text)
        except Exception:
            self.logger.error(f"error {file_name}",exc_info=True)
            raise
        
    def run(self):
        try:
            fs = gridfs.GridFS(self.mongodb.db, self.mongodb.collection)
            all_files = fs.find({})
            for file in all_files:
                self.handle_file(file)
        except Exception:
            self.logger.error("error in running",exc_info=True)
        

