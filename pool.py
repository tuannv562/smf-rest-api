from storage_attribute import StorageAttribute
import logging
import logging.config
from config import LOG_SETTING, HttpCode, HttpMethod
from server import Server
from constant import *
import time
from ldisk import Ldisk

logger = logging.getLogger(__name__)
logging.config.dictConfig(LOG_SETTING)


class Pool(StorageAttribute):
    def __init__(self, server: Server, storage_ip, lower, upper):
        if not lower:
            lower = 0
        if not upper:
            upper = 255
        super().__init__(server, storage_ip, lower, upper)

    def remove(self):
        pool_map = self.__get_all_ldisk_of_pools()
        print('Pool info: {}'.format(pool_map))
        for key, value in pool_map.items():
            if key >= self.lower and key <= self.upper:
                if len(value) > 0:
                    ldisk = Ldisk(self.server, self.storage_ip,
                                min(value), max(value))
                    ldisk.remove()
                self.__remove_pool(key)

    def __get_all_ldisk_of_pools(self):
        _, response_map = self.server.send_request(
            HttpMethod.GET.value, URI_GET_POOL_DETAIL.format(self.storage_ip))
        pool_ldisks_map = {}
        pool_maps = response_map[SMF_KEY_POOLS]
        for pool_map in pool_maps:
            volume_maps = pool_map[SMF_KEY_STORAGE_VOLUMES]
            volumes = []
            for volume_map in volume_maps:
                volumes.append(int(volume_map[SMF_KEY_DEVICE_ID]))
            print(volumes)
            pool_ldisks_map[int(pool_map[SMF_KEY_POOL_ID])] = volumes
        return pool_ldisks_map

    def __remove_pool(self, pool):
        result, message = self.server.send_sync_request(HttpMethod.DELETE.value, URI_DEL_POOL.format(
            pool, self.storage_ip), {}, HttpCode.OK.value, MSG_DELETING_POOL)
        if result:
            logger.info('Delete pool {} successfully'.format(pool))
            print('Delete pool {} successfully'.format(pool))
        else:
            logger.info('Delete pool {} failed. Error message: {}'.format(
                pool, response_map[SMF_KEY_ERROR_DESCRIPTION]))
            print('Delete pool {} failed'.format(pool))
