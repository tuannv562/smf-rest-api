import logging
import logging.config
import http.client
import json
from config import LOG_SETTING, HttpCode

logger = logging.getLogger(__name__)
logging.config.dictConfig(LOG_SETTING)

URI_TOKEN = '/token'
TOKEN_STRING = 'abcd{}{}'
SMF_TOKEN_ACCESS = 'access_token'
HTTP_METHOD_POST = 'POST'


class Server(object):
    def __init__(self, url, port, username, password):
        self.url = url
        self.port = port
        self.username = username
        self.__password = password
        self.__token = self._get_token()
        logger.info('Initialize server with uri: {0}, port: {1}'.format(
            self.url, self.port))

    def _get_token(self):
        conn = http.client.HTTPConnection(
            '{0}:{1}'.format(self.url, self.port, URI_TOKEN))
        headers = {'Content-Type': 'Application/json'}
        params = TOKEN_STRING.format(self.username, self.__password)
        conn.request(HTTP_METHOD_POST, URI_TOKEN, params, headers)
        response = conn.getresponse()
        if response.status == HttpCode.OK:
            data_string = response.read()
            data_map = json.loads(data_string)
            return data_map[SMF_TOKEN_ACCESS]
        else:
            pass
