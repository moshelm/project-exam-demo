import logging 
from config import ServiceConfig

config = ServiceConfig()
config.validate()

logger = logging.basicConfig(
    level=config.level_log,
    format="",
    
)