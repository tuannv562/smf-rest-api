from storage_attribute import StorageAttribute
import logging
import logging.config
from config import LOG_SETTING, HttpCode, HttpMethod
from constant import *

logger = logging.getLogger(__name__)
logging.config.dictConfig(LOG_SETTING)


class Cache(StorageAttribute):
    def __init__(self, server, storage_ip, lower, upper):
        super().__init__(server, storage_ip, lower, upper)

    def remove(self):
        caches_info = list(self.__get_all_cache())
        ldisks_on_wbc = list(self.__get_all_ldisk_on_wbc())
        for ldisk in ldisks_on_wbc:
            self.__set_wbc_for_ldisks(ldisk, False)
        caches = []
        for cache in caches_info:
            caches.append(cache[0])
            if len(cache[2]) != 0:
                self.__unassign_cache_of_ldisk(cache[1], cache[2])

    def __remove_caches(self):
        pass

    def __get_all_cache(self):
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

    def __get_all_ldisk_on_wbc(self):
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

    def __set_wbc_for_ldisks(self, ldisk, state):
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

    def __unassign_cache_of_ldisk(self, cache_type, ldisks):
        param_map = {}
        param_map[SMF_KEY_ACCESS_PATH] = self.storage_ip
        param_map[SMF_KEY_VOLUME_IDS] = ldisks
        param_map[SMF_KEY_CACHE_TYPE] = cache_type
        (status, response_map) = self.server.send_request(
            HttpMethod.PUT.value, URI_MOD_UNASSIGN_CACHE, param_map)
        if status == HttpCode.ACCEPTED.value:
            return True
        else:
            logger.info('unassign cache of ldisk failed. Error message: {}'.format(
                response_map[SMF_KEY_ERROR_DESCRIPTION]))
            return False
