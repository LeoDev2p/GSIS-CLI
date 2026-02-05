from .config import LOG_FILE
import logging

logging.basicConfig(
    filename = LOG_FILE, 
    level=logging.INFO,
    format='%(asctime)s | %(name)-12s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)

def get_logger(name):
    return logging.getLogger(name)
