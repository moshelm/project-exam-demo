from elasticsearch import Elasticsearch
from logging import Logger

class ElasticConnection():
    def __init__(self,elastic_config:str, index_name:str, logger :Logger):
        try:
            self.es = Elasticsearch(elastic_config)
        except Exception:
            raise
        self.index = index_name
        self.logger = logger

    def insert(self,data:dict,file_id:str):
        try:
            self.es.index(index= self.index, document= data, id= file_id)
            self.logger.info("success insert new doc to elastic")
        except Exception:
            self.logger.error("failed insert to elastic",exc_info=True)
    
    def search(self,query:dict):
        try:
            result = self.es.search(index=self.index, body= query)
            return result
        except Exception:
            self.logger.error("failed to search this query",exc_info=True)
    
    def add_new_filed(self,file_id: str, new_field:dict):
        try:
            result = self.es.update(index=self.index, id=file_id, doc=new_field, doc_as_upsert=True)
        except Exception:
            self.logger.error(f"failed update doc id:{file_id}",exc_info=True)
    
    def get_index_by_id(self,doc_id:str):
        return self.read_result(self.es.get(index= self.index, id= doc_id))

    def read_result(self,result):
        data = []
        for hit in result['hits']['hits']:
            data.append(hit)
        return data