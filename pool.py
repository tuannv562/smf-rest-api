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
                ldisk = Ldisk(self.server, self.storage_ip,
                              min(value), max(value))
                ldisk.remove()

    def __get_all_ldisk_of_pools(self):
        _, response_map = self.server.send_request(
            HttpMethod.GET.value, URI_GET_ALL_VOLUME_DETAIL.format(self.storage_ip))
        volume_maps = response_map[SMF_KEY_VOLUMES]
        pool_map = {}
        for volume_map in volume_maps:
            pool = int(volume_map[SMF_KEY_POOL_ID])
            if pool in pool_map:
                volumes = pool_map[pool]
                volumes.append(int(volume_map[SMF_KEY_DEVICE_ID]))
            else:
                pool_map[pool] = [int(volume_map[SMF_KEY_DEVICE_ID])]
        return pool_map
