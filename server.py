import logging
import logging.config
import http.client
import json
import time
from config import LOG_SETTING, HttpCode, HttpMethod

logger = logging.getLogger(__name__)
logging.config.dictConfig(LOG_SETTING)

URI_TOKEN = '/tokens'
TOKEN_STRING = 'grant_type=password&client_id=my-trusted-client-with-secret&client_secret=somesecret&username={}&password={}'
HEADER_AUTHENTICATION = 'Bearer {}'
SMF_KEY_TOKEN_ACCESS = 'access_token'
SMF_KEY_ERROR_DESCRIPTION = 'error_description'


class Server(object):
    def __init__(self, url, port, username, password):
        self.url = url
        self.port = port
        self.username = username
        self.__password = password
        self.__token = self.__get_token()
        logger.info('Initialize server successfully with url: {0}, port: {1}'.format(
            self.url, self.port))

    def __get_token(self):
        try:
            conn = http.client.HTTPConnection(
                self.url, port=self.port, timeout=20)
            headers = {'Content-Type': 'application/x-www-form-urlencoded',
                       'Accept': 'application/json'}
            params = TOKEN_STRING.format(self.username, self.__password)
            conn.request(HttpMethod.POST.value, URI_TOKEN, params, headers)
            response = conn.getresponse()
            content = bytes.decode(response.read(), 'utf-8')
            if response.status == HttpCode.OK.value:
                token_map = json.loads(content)
                return token_map[SMF_KEY_TOKEN_ACCESS]
            else:
                response_map = json.loads(content)
                logger.info(response_map[SMF_KEY_ERROR_DESCRIPTION])
                raise ValueError(response_map[SMF_KEY_ERROR_DESCRIPTION])
        except Exception as ex:
            raise ex
        finally:
            conn.close()

    def send_request(self, method, uri, content_map={}):
        logger.info('Send request with method: {}, uri: {}, content: {}'.format(
            method, uri, json.dumps(content_map)))
        try:
            conn = http.client.HTTPConnection(
                self.url, port=self.port, timeout=20)
            headers = {'Content-Type': 'application/json',
                       'Accept': 'application/json',
                       'Authorization': HEADER_AUTHENTICATION.format(self.__token)}
            params = json.dumps(content_map)
            conn.request(method, uri, params, headers)
            response = conn.getresponse()
            content = bytes.decode(response.read(), 'utf-8')
            logger.info(
                'Send request successfully. Return code: {}'.format(response.status))
            return (response.status, json.loads(content))
        except Exception as ex:
            logger.info('Send request failed')
            raise ex
        finally:
            conn.close()

    def send_sync_request(self, method, uri, content_map, success_code, wait_msg):
        logger.info(
            'Send sync request with method: {}, uri: {}'.format(method, uri))
        while True:
            (status, response_map) = self.send_request(method, uri, content_map)
            if status == success_code:
                logger.info('Send sync request successfully')
                return (True, '')
            else:
                if response_map[SMF_KEY_ERROR_DESCRIPTION] == wait_msg:
                    time.sleep(10)
                    continue
                else:
                    logger.info('Send sync request failed')
                    return (False, response_map[SMF_KEY_ERROR_DESCRIPTION])
