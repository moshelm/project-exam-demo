from pymongo import MongoClient
from pymongo.errors import PyMongoError
import os 
from logging import Logger

class MongoConnection():
    def __init__(self,mongo_config:str, mongo_database:str, logger:Logger):
        self.logger = logger
        try:
            self.client = MongoClient(mongo_config)
        except PyMongoError:
            self.logger.critical("connection mongodb failed",exc_info=True)
        
        self.db = self.client[mongo_database]

    def insert(self):
        pass            

