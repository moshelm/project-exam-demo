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
            return self.read_result(result)
        except Exception:
            self.logger.error("failed to search this query",exc_info=True)
            
    def get_index_by_id(self,doc_id:str):
        return self.read_result(self.es.get(index= self.index, id= doc_id))

    def read_result(self,result):
        data = []
        for hit in result['hits']['hits']:
            data.append(hit)
        return data