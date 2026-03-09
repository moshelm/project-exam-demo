from shared.elasticsearch_connection import ElasticConnection
from shared.kafka.consumer import KafkaConsumer
from logging import Logger
from lists_analyze import ListHostile

class Analyzer():
    def __init__(self,hostile, less_hostile, consumer:KafkaConsumer, elastic:ElasticConnection, logger: Logger):
        self.logger = logger 
        self.consumer = consumer
        self.hostile_list = hostile
        self.less_hostile_list = less_hostile
        self.es = elastic

    def encoded_lists(self):
        encode = ListHostile(self.hostile_list, self.less_hostile_list, self.logger)
        lists_encoded = encode.run()
        self.hostile_list = lists_encoded['hostile_list']
        self.less_hostile_list = lists_encoded['less_hostile_list']

    def score(self,doc_id):
        try:
            should_words = []
            for word in self.hostile_list:
                should_words.append({
                    'match_phrase':{
                        'data_stt':{
                            'query': word,
                            'boost': 2.0
                        }
                    }
                })
            for word in self.less_hostile_list:
                should_words.append({
                    'match_phrase':{
                        'data_stt':{
                            'query':word,
                            'boost':1.0
                        }
                    }
                })
            query = {'query':{
                'bool':{
                    'must':[{'term':{'_id':doc_id}}],
                    'should': should_words,
                    'minimum_should_match':1  
                }
            }}
            return self.es.search(query)
        except Exception:
            self.logger.error("failed get score")
            raise


    def analyze_score(self,doc_id:dict):
        try:
            doc_id = doc_id['_id']
            doc = self.score(doc_id)['hits']['hits']
            self.logger.info(f'get from search. {doc}')
            bds_percent = 0
            is_bds = False
            bds_by_level = 'None'
            if doc:
                doc = doc[0] 
                total_words = len(doc['_source']['data_stt'].split(' '))
                bds_percent = int((doc['_score'] / total_words ) * 100) + 1
                if bds_percent >= 10:
                    is_bds = True
                    bds_by_level = 'high'
                elif 5 <= bds_percent < 10:
                    bds_by_level = 'medium'
            return doc_id,{'is_bds':is_bds,
                           'bds_threat_level':bds_by_level,
                           'bds_percent':bds_percent}
        except Exception:
            self.logger.error('bad results from elastic',exc_info=True)


    def handel_event(self,doc:dict):
        try:
            self.es.refresh_index()
            doc_id, doc_status = self.analyze_score(doc)
            self.es.add_new_filed(doc_id, doc_status)
            self.logger.info(f'update doc. {doc_id}')
        except Exception:
            self.logger.error('failed update docs')

    def run(self):
        try:
            self.encoded_lists()
            self.consumer.run(self.handel_event)
        except Exception:
            self.logger.error('failed',exc_info=True)
