import os 

class ServiceConfig():
    def __init__(self):
        kafka_port = os.getenv("KAFKA_PORT","9092")
        kafka_host = os.getenv("KAFKA_HOST","localhost")
        
        self.topics = os.getenv("TOPICS","open").split(',')
        self.group_id = os.getenv("GROUP_ID","open")

        self.kafka_connect= {
            "bootstrap.servers":f"{kafka_host}:{kafka_port}",
            "group.id":self.group_id,
            "auto.offset.reset":"earliest"}
        
        mongo_host = os.getenv("MONGO_HOST","localhost")
        mongo_port = os.getenv("MONGO_PORT","27017")

        self.mongo_config = f"mongodb://{mongo_host}:{mongo_port}"
        self.mongo_db = os.getenv("MONGO_DATABASE","audio")
        self.mongo_collection = os.getenv("MONGO_COLLECTION","audio")

        elasticsearch_host = os.getenv("ELASTICSEARCH_HOST","localhost")
        elasticsearch_port = os.getenv("ELASTICSEARCH_PORT","9200")
        self.index_name = os.getenv("INDEX_NAME","audio")
        self.index_logger = os.getenv("INDEX_LOGGER","logger")

        self.elastic_config = f"http://{elasticsearch_host}:{elasticsearch_port}"

        self.level_log = os.getenv("LEVEL_LOG","INFO")
        self.service_name = os.getenv("SERVICE_NAME","process-files")
        
        self.language = os.getenv("LANGUAGE",'en-US')
    def validate(self):
        if not self.kafka_connect:
            raise