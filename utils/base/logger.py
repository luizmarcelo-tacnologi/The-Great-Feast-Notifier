import logging
from logging.handlers import RotatingFileHandler
import utils.base.configpath as cfgp

#Sets the logger
logger = logging.getLogger("TheGreatFeastNotifier")
logger.setLevel(logging.INFO)

#Logger initialization
def init_logger():
    #Sets the handler
    handler = RotatingFileHandler(
        cfgp.log_path,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8"
    )
    #Sets the handler formating
    handler.setFormatter(logging.Formatter("[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    #Sets the logger handler to be the previously defined handler
    logger.addHandler(handler)

#The logging
def log(message):
    logger.info(message)