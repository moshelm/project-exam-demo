from logging import Logger
from pathlib import Path
from datetime import datetime

class OpenFiles():
    def __init__(self, data_path: Path, logger:Logger):
        self.logger = logger
        self.path_to_dir = data_path
    
    def get_file_metadata(self,file:str):
            file_path = self.data_path / file
            if not file_path.exists():
                 self.logger.error("not found file",exc_info=True)
                 raise FileNotFoundError
            stats = file_path.stat()
            metadata = {
                    "file_name":file_path.name,
                    "file_size" : stats.st_size,
                    "file_create_date": datetime.fromtimestamp(stats.st_birthtime)
                    }
            return  {
                 "file_path":str(file_path),
                 "metadata":metadata
                 }
            