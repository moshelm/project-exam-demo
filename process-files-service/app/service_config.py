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
        data_path = os.getenv("DATA_PATH","/data")

        self.data_path = Path(data_path) / "podcasts"
    def validate(self):
        if not self.kafka_connect:
            raise