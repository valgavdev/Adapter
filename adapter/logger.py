import logging

from .logcustom import Logger
from . import config

http_logger = Logger(logging.getLogger(__name__))
http_logger.init(config.log_format, logging.INFO)
