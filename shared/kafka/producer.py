from logging import Logger
from confluent_kafka import Producer, Message , KafkaException
from shared.utils.serialize_json import serialize_json

class KafkaProducer():
    def __init__(self,kafka_connection:dict, topic:str, logger:Logger):
        self.logger = logger 
        self.topic = topic
        config = kafka_connection 
        config['logger'] = logger
        try: 
            self.producer = Producer(config)
        except KafkaException:
            self.logger.critical("kafka producer failed in connection",exc_info=True)
            raise
    def delivery_back(self,err:Message, msg: Message):
        if err is not None:
            self.logger.error("Delivery failed for Message: {} : {}".format(msg.value(), err))
            return
        self.logger.info('Message: {} successfully produced to Topic: {} Partition: [{}] at offset {}'.format(
         msg.value(), msg.topic(), msg.partition(), msg.offset()))

    def send_event(self,data:dict):
        try:
            self.logger.info("serialize data to json encoded")
            value = serialize_json(data)
            self.logger.info("send new event...")
            self.producer.produce(topic=self.topic, value=value, callback=self.delivery_back)
        
        except KafkaException:
            self.logger.critical("error in produce",exc_info=True)
            raise
        except Exception:
            self.logger.error("error to send event",exc_info=True)
            raise

    def close(self):
        try:
            self.producer.flush()
        except Exception:
            self.logger.error("flush failed",exc_info=True)