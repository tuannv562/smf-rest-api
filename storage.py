import logging
import logging.config
from server import Server
from config import LOG_SETTING, HttpCode, HttpMethod


logger = logging.getLogger(__name__)
logging.config.dictConfig(LOG_SETTING)

URI_CHECK_STORAGE_IP = '/smf_api/enclosures/?accesspath={}&type=SC3000'
URI_GET_ALL_VOLUMES = '/smf_api/volumes/?accesspath={}'
URI_DEL_LDISK = '/smf_api/volumes/{}/?accesspath={}'
SMF_KEY_LDISK_VOLUMES = 'volumes'
SMF_KEY_LDISK_DEVICE_ID = 'deviceId'
MSG_CREATING_LDISK = ' Processing the volume definition'


class Storage(object):
    def __init__(self, server, ip):
        self.server = server
        self.ip = ip
        (status, _) = self.server.send_request(HttpMethod.GET.value,
                                               uri=URI_CHECK_STORAGE_IP.format(self.ip))
        if status != HttpCode.OK.value:
            logger.info('Storage IP is not available')
            raise ValueError('Storage IP not available')
        logger.info('Initialize Storage successfully with IP: {}'.format(ip))

    def remove(self, attribute_type, lower_id, upper_id):
        pass

    def _remove_ldisks(self, lower_id, upper_id):
        volume_list = list(self._get_all_volume_id())
        for i, ldisk_id in enumerate(list):
            if ldisk_id >= lower_id and ldisk_id <= upper_id:
                self._remove_ldisk(ldisk_id)
            else:
                break

    def _remove_ldisk(self, ldisk_id):
        (result, msg) = self.server.send_sync_request(HttpMethod.DELETE.value,
                                                      URI_DEL_LDISK.format(ldisk_id, self.ip), {}, HttpCode.OK.value, MSG_CREATING_LDISK)
        if result:
            logger.info('Remove LDISK {} successfully'.format(ldisk_id))
            return True
        else:
            pass

    def _get_all_volume_id(self):
        (status, content_map) = self.server.send_request(
            HttpMethod.GET.value, URI_GET_ALL_VOLUMES.format(self.ip))
        if status == HttpCode.OK.value:
            volumes_map = content_map[SMF_KEY_LDISK_VOLUMES]
            for volume_map in volumes_map:
                yield int(volume_map[SMF_KEY_LDISK_DEVICE_ID])
        else:
            logger.info('get all ldisk ID failed')
            raise Exception('Can not get all LDISK iD')
