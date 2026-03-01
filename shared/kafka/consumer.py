from confluent_kafka import Consumer, Message, KafkaException
from logging import Logger 


class KafkaConsumer():
    def __init__(self,kafka_connection:str, topics:list[str], logger:Logger):
        self.logger = logger
        config = kafka_connection 
        config['logger'] = logger
        try: 
            self.consumer = Consumer(config)
        except KafkaException:
            self.logger.critical("kafka consumer failed in connection",exc_info=True)
            raise
        self.topics = topics
        
    def run(self,callback):
        try:
            self.consumer.subscribe(self.topics)
            while True:
                msg = self.consumer.poll()
                if msg is None:
                    continue
                if msg.error():
                    self.logger.error(f"error in msg. {msg.error()}")
                    continue
                self.logger.info("get new event...")
                value = msg.value()
                callback(value)
        except KafkaException:
            self.logger.critical("consumer failed",exc_info=True)
            raise
        except Exception:
            self.logger.error("consumer failed",exc_info=True)
            raise



    