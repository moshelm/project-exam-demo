import pathlib
import json 
from logging import Logger
from pathlib import Path
import os 
from datetime import datetime

class OpenFiles():
    def __init__(self, data_path: Path, logger:Logger):
        self.logger = logger
        self.path_to_dir = data_path
    
    def get_file_metadata(self,file:str):
            file_path = os.path.join(self.path_to_dir,file)
            file_name = os.path.basename(file_path)
            metadata = {
                  "file_name":file_name,
                "file_size" : os.path.getsize(file_path),
                "date_create": datetime.fromtimestamp(os.path.getctime(file_path))
            }
            return  {"file_path":file_path,
                     "metadata":metadata}
            