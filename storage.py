import logging
import logging.config
from server import Server
from config import LOG_SETTING


logger = logging.getLogger(__name__)
logging.config.dictConfig(LOG_SETTING)


class Storage(object):
    def __init__(self, server, ip):
        self.server = server
        self.ip = ip
        logger.info('Initialize Storage with IP: {}'.format(ip))

    def remove(self, attribute_type, lower_id, upper_id):
        pass
