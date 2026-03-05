import logging 
from manager import Orchestrator
from service_config import ServiceConfig
from shared.elasticsearch_connection import ElasticConnection
from shared.logger_elastic import Logger
from shared.mongo_connection import MongoConnection

config = ServiceConfig()
config.validate()

logging.getLogger("pymongo").setLevel(logging.ERROR)
logging.getLogger("elasticsearch").setLevel(logging.ERROR)
logging.getLogger("confluent_kafka").setLevel(logging.ERROR)

logger = Logger.get_logger(config.service_name, config.elastic_config, config.index_logger)

# logging.basicConfig(
#     level=config.level_log,
#     format=f'%(asctime)s | {config.service_name} | %(name)s - %(levelname)s -  %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S'
# )

# consumer_logger = logging.getLogger("consumer")
# file_processor_logger = logging.getLogger("file_processor")
# manager_logger = logging.getLogger("manager")
# mongo_logger = logging.getLogger("mongodb")
# elastic_logger = logging.getLogger("elastic")
# mongo_tor_logger = logging.getLogger("stor gridfs")


def main():
    try:
        mongodb = MongoConnection(config.mongo_config, config.mongo_db, config.mongo_collection, logger)
        elastic = ElasticConnection(config.elastic_config, config.index_name, logger)
        manager = Orchestrator(elastic, mongodb, config.language, logger)

        manager.run()
    except Exception:
        raise

if __name__=="__main__":
    try:
        main()
    except Exception:
        raise