import gridfs
from gridfs.errors import FileExists,GridFSError
from logging import Logger
from shared.mongo_connection import MongoConnection

class StorAudioMongo():
    def __init__(self,mongo_config:str, mongo_database:str,logger: Logger):
        self.logger = logger
        self.mongo = MongoConnection(mongo_config,mongo_database,logger)
        try:
            self.fs = gridfs.GridFS(self.mongo.db,"audio-collection")
        except GridFSError:
            self.logger.error("error in gridfs")
            raise
        
    
    def insert(self,file_name:str, voice,file_id:str):
        try:
            mongo_id = self.fs.put(voice,file_id=file_id,filename=file_name)
            self.logger.info(f"new file in mongo db id:{mongo_id}")
        except FileExists:
            self.logger.error("gridfs file exists",exc_info=True)
        except GridFSError:
            self.logger.error("error in gridfs",exc_info=True)
            raise


