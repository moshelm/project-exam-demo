import base64
import os 
from logging import Logger

class ListHostile():
    def __init__(self,hostile, less_hostile, logger: Logger):
        self.logger = logger
        self.hostile_list = hostile
        self.less_hostile_list = less_hostile
        
    def decoded_base64(self,code:str):
        return base64.b64decode(code).decode()
    
    def run(self):
        try:
            return {
             "hostile_list":self.decoded_base64(self.hostile_list).split(','),
            "less_hostile_list":self.decoded_base64(self.less_hostile_list).split(',')}
        except Exception:
            self.logger.critical("failed decoded lists",exc_info=True)
            raise

