import os 

class ServiceConfig():
    def __init__(self):
        kafka_port = os.getenv("KAFKA_PORT","9092")
        kafka_host = os.getenv("KAFKA_HOST","localhost")
        
        self.topics_consumer = os.getenv("TOPICS_CONSUMER","analyze").split(',')
        self.group_id = os.getenv("GROUP_ID","analyze")

        self.kafka_connect= {
            "bootstrap.servers":f"{kafka_host}:{kafka_port}",
            "group.id":self.group_id,
            "auto.offset.reset":"earliest"}
        
        elasticsearch_host = os.getenv("ELASTICSEARCH_HOST","localhost")
        elasticsearch_port = os.getenv("ELASTICSEARCH_PORT","9200")
        self.index_name = os.getenv("INDEX_NAME","audio")
        self.index_logger = os.getenv("INDEX_LOGGER","logger")

        self.elastic_config = f"http://{elasticsearch_host}:{elasticsearch_port}"
        self.hostile_list = os.getenv("HOSTILE_LIST","SDA")
        self.less_hostile_list = os.getenv("LESS_HOSTILE_LIST","SDA")
        self.level_log = os.getenv("LEVEL_LOG","INFO")
        self.service_name = os.getenv("SERVICE_NAME","process-files")
        
    def validate(self):
        if not self.elastic_config:
            raise