import os 
from pathlib import Path

class ServiceConfig():
    def __init__(self):
        kafka_port = os.getenv("KAFKA_PORT","9092")
        kafka_host = os.getenv("KAFKA_HOST","localhost")
        
        self.topic = os.getenv("TOPIC","open")

        self.kafka_connect= {"bootstrap.servers":f"{kafka_host}:{kafka_port}"}

        self.level_log = os.getenv("LEVEL_LOG","INFO")
        self.service_name = os.getenv("SERVICE_NAME","process-files")
        
        elasticsearch_host = os.getenv("ELASTICSEARCH_HOST","localhost")
        elasticsearch_port = os.getenv("ELASTICSEARCH_PORT","9200")
        self.index_logger = os.getenv("INDEX_LOGGER","logger")
        self.elastic_config = f"http://{elasticsearch_host}:{elasticsearch_port}"

        data_path = os.getenv("DATA_PATH","/data")

        self.data_path = Path(data_path) / "podcasts"
    
    def validate(self):
        if not self.kafka_connect:
            raise