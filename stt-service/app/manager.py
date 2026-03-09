from shared.elasticsearch_connection import ElasticConnection
from shared.mongo_connection import MongoConnection
from shared.kafka.consumer import KafkaConsumer, KafkaException
from shared.kafka.producer import KafkaProducer
from logging import Logger 
import gridfs
from stt import stt_file
from io import BytesIO

class Orchestrator():
    def __init__(self,elastic : ElasticConnection, mongodb : MongoConnection, producer : KafkaProducer, consumer : KafkaConsumer, language:str, logger : Logger):
        self.logger = logger 
        self.language = language
        self.consumer = consumer
        self.producer = producer
        self.elastic = elastic
        self.mongodb = mongodb
        self.fs = gridfs.GridFS(self.mongodb.db, self.mongodb.collection)
        
    def handle_file(self, data:dict):
        try:
            file_id = data['file_id']
            result = self.fs.find_one({"file_id":file_id})
            file_name = getattr(result,'filename','unknown_name')
            self.logger.info("find the file in mongo")
            file_bytes = result.read()
            file_for_memory = BytesIO(file_bytes)
            file_text = stt_file(file_for_memory, self.language)
            self.logger.info(f"success stt process for id:{file_id}")
            data = {"data_stt":file_text}
            res = self.elastic.add_new_filed(file_id,data)
            self.logger.info(f"success update in elastic {file_name}. result:{str(res)}")
            self.producer.send_event({'_id':file_id})
        except Exception:
            self.logger.error(f"error {file_name}",exc_info=True)
            raise
        
    def run(self):
        try:
            self.consumer.run(self.handle_file)
        except KafkaException:
            self.logger.error("kafka failed",exc_info=True)
            raise
        except Exception:
            self.logger.error("error in running",exc_info=True)
        

