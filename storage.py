import logging
import logging.config
from server import Server
from config import LOG_SETTING, HttpCode, HttpMethod


logger = logging.getLogger(__name__)
logging.config.dictConfig(LOG_SETTING)

URI_CHECK_STORAGE_IP = '/smf_api/enclosures/?accesspath={}&type=SC3000'
URI_GET_ALL_VOLUMES = '/smf_api/volumes/?accesspath={}'
URI_GET_ALL_VOLUME_DETAIL = '/smf_api/volumes/detail?accesspath={}'
URI_GET_ALL_CACHE = '/smf_api/cachepartition/?accesspath={}'
URI_DEL_LDISK = '/smf_api/volumes/{}/?accesspath={}'
URI_SPLIT_REPLICATION = '/smf_api/replications/mirrors/{}'
URI_DEL_OBR = '/smf_api/replications/mirrors/{}/?accesspath={}&force=true&mode=remote'
URI_DEL_IBR = '/smf_api/replications/mirrors/{}/?accesspath={}&force=true&mode=local'
URI_DEL_SNAPSHOT = '/smf_api/replications/snapshots/{}?accesspath={}'
URI_DEL_CACHE = '/smf_api/cachepartition/?accesspath={}&inelements={}'
URI_DEL_POOL = '/smf_api/pools/{}?accesspath={}'
URI_GET_ALL_LDISK_IN_POOL = '/smf_api/pools/{}/?accesspath={}'
URI_MOD_LDISK = '/smf_api/volumes/{}'
URI_MOD_WBC = '/smf_api/writebackcache'

SMF_KEY_VOLUMES = 'volumes'
SMF_KEY_TOSHIBA_WBC = 'toshibaWBC'
SMF_KEY_DEVICE_ID = 'deviceId'
SMF_KEY_ENABLE_TIER = 'enableTier'
SMF_KEY_ACCESS_PATH = 'accessPath'
SMF_KEY_ERROR_DESCRIPTION = 'error_description'
SMF_KEY_MODE = 'mode'
SMF_KEY_FORCE = 'force'
SMF_KEY_CACHE_PARTITIONS = 'cachePartitions'
SMF_KEY_TOSHIBA_CACHE_PARTITION_ID = 'toshibaCachePartitionID'
SMF_KEY_WRITE_BACK_CACHE_STATUS = 'writeBackCacheStatus'
SMF_KEY_VOLUME_ID = 'volumeId'
SMF_KEY_TOSHIBA_CACHE_TYPE = 'toshibaCacheType'
MSG_CREATING_LDISK = ' Processing the volume definition'


class Storage(object):
    def __init__(self, server, storage_ip):
        self.server = server
        self.storage_ip = storage_ip
        (status, _) = self.server.send_request(HttpMethod.GET.value,
                                               uri=URI_CHECK_STORAGE_IP.format(self.storage_ip))
        if status != HttpCode.OK.value:
            logger.info('Storage IP is not available')
            raise ValueError('Storage IP not available')
        logger.info(
            'Initialize Storage successfully with IP: {}'.format(storage_ip))

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
                                                      URI_DEL_LDISK.format(ldisk_id, self.storage_ip), {}, HttpCode.OK.value, MSG_CREATING_LDISK)
        if result:
            logger.info('Remove LDISK {} successfully'.format(ldisk_id))
            return True
        else:
            pass

    def _get_all_volume_id(self):
        (status, content_map) = self.server.send_request(
            HttpMethod.GET.value, URI_GET_ALL_VOLUMES.format(self.storage_ip))
        if status == HttpCode.OK.value:
            volumes_map = content_map[SMF_KEY_VOLUMES]
            for volume_map in volumes_map:
                yield int(volume_map[SMF_KEY_DEVICE_ID])
        else:
            logger.info('get all ldisk ID failed')
            raise Exception('Can not get all LDISK iD')

    def _remove_obr(self, ldisk_id):
        # split mirror set
        logger.info('Split OBR of LDISK {}'.format(ldisk_id))
        content_map = {SMF_KEY_ACCESS_PATH: self.storage_ip,
                       'operation': 'split', SMF_KEY_MODE: 'remote',
                       SMF_KEY_FORCE: 'true'}
        self.server.send_request(HttpMethod.PUT.value,
                                 URI_SPLIT_REPLICATION.format(ldisk_id), content_map)
        # remove obr
        (status, response_map) = self.server.send_request(
            HttpMethod.DELETE.value, URI_DEL_OBR.format(ldisk_id, self.storage_ip))
        if status == HttpCode.OK.value:
            logger.info('Delete OBR of LDISK {} successfully'.format(ldisk_id))
            return True
        else:
            logger.info('Delete OBR of LDISK {} failed. Error message: {}'.format(
                ldisk_id, response_map[SMF_KEY_ERROR_DESCRIPTION]))
            return False

    def _remove_ibr(self, ldisk_id):
        # split mirror set
        logger.info('Split IBR of LDISK {}'.format(ldisk_id))
        content_map = {SMF_KEY_ACCESS_PATH: self.storage_ip,
                       'operation': 'split', SMF_KEY_MODE: 'local',
                       SMF_KEY_FORCE: 'true'}
        self.server.send_request(HttpMethod.PUT.value,
                                 URI_SPLIT_REPLICATION.format(ldisk_id), content_map)
        # remove ibr
        (status, response_map) = self.server.send_request(
            HttpMethod.DELETE.value, URI_DEL_IBR.format(ldisk_id, self.storage_ip))
        if status == HttpCode.OK.value:
            logger.info('Delete IBR of LDISK {} successfully'.format(ldisk_id))
            return True
        else:
            logger.info('Delete IBR of LDISK {} failed. Error message: {}'.format(
                ldisk_id, response_map[SMF_KEY_ERROR_DESCRIPTION]))
            return False

    def _remove_snapshot(self, ldisk_id):
        (status, response_map) = self.server.send_request(
            HttpMethod.DELETE.value, ldisk_id, self.storage_ip)
        if status == HttpCode.OK.value:
            logger.info(
                'Delete LDISK snapshot {} successfully'.format(ldisk_id))
            return True
        else:
            logger.info('Delete LDISK snapshot {} failed. Error message: {}'.format(
                ldisk_id, response_map[SMF_KEY_ERROR_DESCRIPTION]))
            return False

    def _disable_tiering(self, ldisk_id):
        param_map = {SMF_KEY_ACCESS_PATH: self.storage_ip,
                     SMF_KEY_ENABLE_TIER: 'false'}
        (status, response_map) = self.server.send_request(
            HttpMethod.PUT.value, URI_MOD_LDISK.format(ldisk_id), param_map)
        if status == HttpCode.OK.value:
            logger.info(
                'Disable tiering of LDISK {} successfully'.format(ldisk_id))
            return True
        else:
            logger.info('Disable tiering of LDISK {} failed. Error message: {}'.format(
                ldisk_id, response_map[SMF_KEY_ERROR_DESCRIPTION]))
            return False

    def _remove_caches(self, lower, upper):
        caches = list(self._get_all_cache_id())
        lidks_on_wbc = list(self._get_all_ldisk_on_wbc())
        for ldisk in lidks_on_wbc:
            self._set_wbc_for_ldisks(ldisk, False)

    def _remove_cache(self, cache_id):
        (status, response_map) = self.server.send_request(
            HttpMethod.DELETE.value, URI_DEL_CACHE.format(self.storage_ip, cache_id))
        if status == HttpCode.OK.value:
            logger.info(
                'Delete cache partition {} successfully'.format(cache_id))
            return True
        else:
            logger.info('Delete cache partition {} failed. Error message: {}'.format(
                cache_id, response_map[SMF_KEY_ERROR_DESCRIPTION]))
            return False

    def _get_all_cache_id(self):
        (status, response_map) = self.server.send_request(
            HttpMethod.GET.value, URI_GET_ALL_CACHE.format(self.storage_ip))
        if status == HttpCode.OK.value:
            cache_maps = response_map[SMF_KEY_CACHE_PARTITIONS]
            for cache_map in cache_maps:
                try:
                    cache_id = int(
                        cache_map[SMF_KEY_TOSHIBA_CACHE_PARTITION_ID])
                    volumes = []
                    if cache_map[SMF_KEY_VOLUME_ID] != '---'\
                        and cache_map[SMF_KEY_VOLUME_ID] != 'tiering':
                        volumes = str(cache_map[SMF_KEY_VOLUME_ID]).split(',')
                    yield (cache_id, cache_map[SMF_KEY_TOSHIBA_CACHE_TYPE], volumes)
                except:
                    continue
        else:
            logger.info('Get all cache failed. Error message: {}'.format(
                response_map[SMF_KEY_ERROR_DESCRIPTION]))
            raise Exception('Cannot get information of cache partition')

    def _get_all_ldisk_on_wbc(self):
        (status, response_map) = self.server.send_request(
            HttpMethod.GET.value, URI_GET_ALL_VOLUME_DETAIL.format(self.storage_ip))
        if status == HttpCode.OK.value:
            volume_maps = response_map[SMF_KEY_VOLUMES]
            for volume_map in volume_maps:
                if volume_map[SMF_KEY_TOSHIBA_WBC] == 'ON':
                    yield int(volume_map[SMF_KEY_DEVICE_ID])
        else:
            logger.info('Get all cache failed. Error message: {}'.format(
                response_map[SMF_KEY_ERROR_DESCRIPTION]))
            raise Exception('Cannot get detail information of LDISK')

    def _set_wbc_for_ldisks(self, ldisk, state):
        param_map = {}
        if state:
            param_map[SMF_KEY_WRITE_BACK_CACHE_STATUS] = 'true'
        else:
            param_map[SMF_KEY_WRITE_BACK_CACHE_STATUS] = 'false'
        param_map[SMF_KEY_ACCESS_PATH] = self.storage_ip
        param_map[SMF_KEY_VOLUME_ID] = str(ldisk)
        (status, response_map) = self.server.send_request(
            HttpMethod.POST.value, URI_MOD_WBC, param_map)
        if status == HttpCode.OK.value:
            return True
        else:
            logger.info('set wbc for LDISK {} failed. Error message: {}'.format(
                ldisks, response_map[SMF_KEY_ERROR_DESCRIPTION]))
            return False

    def _unassign_cache_of_ldisk(self, cache, ldisk):
        pass

    def _remove_pool(self, pool_id):
        (status, response_map) = self.server.send_request(
            HttpMethod.DELETE.value, URI_DEL_POOL.format(pool_id, self.storage_ip))
        if status == HttpCode.OK.value:
            logger.info(
                'Delete pool {} successfully'.format(pool_id))
            return True
        else:
            logger.info('Delete pool {} failed. Error message: {}'.format(
                pool_id, response_map[SMF_KEY_ERROR_DESCRIPTION]))
            return False

    def _get_all_ldisk_in_pool(self, pool_id):
        (status, response_map) = self.server.send_request(HttpMethod.GET.value,
                                                          URI_GET_ALL_LDISK_IN_POOL.format(pool_id, self.storage_ip))
        if status == HttpCode.OK.value:
            pass
        else:
            logger.info('Get all LDISK of pool {} failed. Error message: {}'.format(
                pool_id, response_map[SMF_KEY_ERROR_DESCRIPTION]))
            raise Exception('Cannot get detail pool information')
