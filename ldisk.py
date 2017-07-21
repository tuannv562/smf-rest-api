from storage_attribute import StorageAttribute
import logging
import logging.config
from config import LOG_SETTING, HttpCode, HttpMethod
from constant import *

logger = logging.getLogger(__name__)
logging.config.dictConfig(LOG_SETTING)


class Ldisk(StorageAttribute):
    def __init__(self, server, storage_ip, lower, upper):
        super().__init__(server, storage_ip, lower, upper)

    def remove(self):
        all_ldisks = list(self.__get_all_ldisk())
        ldisks = []
        for i in all_ldisks:
            if i < self.lower:
                continue
            elif i > self.upper:
                break
            else:
                ldisks.append(i)
        print('Delete LDISK {}'.format(ldisks))
        for i in ldisks:
            self.__remove_ldisk(i)

    def __get_all_ldisk(self):
        (status, content_map) = self.server.send_request(
            HttpMethod.GET.value, URI_GET_ALL_VOLUMES.format(self.storage_ip))
        if status == HttpCode.OK.value:
            volumes_map = content_map[SMF_KEY_VOLUMES]
            for volume_map in volumes_map:
                yield int(volume_map[SMF_KEY_DEVICE_ID])
        else:
            logger.info('get all ldisk ID failed')
            raise Exception('Can not get all LDISK iD')

    def __remove_ldisk(self, ldisk):
        (status, response_map) = self.server.send_request(
            HttpMethod.DELETE.value, URI_DEL_LDISK.format(ldisk, self.storage_ip))
        if status == HttpCode.OK.value:
            print('Delete LDISK {} successfully'.format(ldisk))
            return True
        else:
            if response_map[SMF_KEY_ERROR_DESCRIPTION] == MSG_DEL_LDISK_TIERING_ENABLE:
                # ldisk enable tiering
                ldisks_enable_tier = list(self.get_all_ldisk_enable_tier())
                for i in ldisks_enable_tier:
                    self.set_tiering_of_ldisk(i, False)
                self.__remove_ldisk(ldisk)
            elif response_map[SMF_KEY_ERROR_DESCRIPTION] == MSG_DEL_LDISK_HAS_SNAPSHOT \
                    or response_map[SMF_KEY_ERROR_DESCRIPTION] == MSG_DEL_SNAPSHOT_LDISK:
                base_ldisk = self.__get_base_ldisk(ldisk)
                if base_ldisk != ldisk:
                    self.__change_current_ldisk(base_ldisk, 'change')
            else:
                logger.info('Delete LDISK {} failed. Error message: {}'.format(
                    ldisk, response_map[SMF_KEY_ERROR_DESCRIPTION]))
                print('Delete LDISK {} failed. Error message: {}'.format(
                    ldisk, response_map[SMF_KEY_ERROR_DESCRIPTION]))
                return False

    def set_tiering_of_ldisk(self, ldisk, state):
        param_map = {}
        param_map[SMF_KEY_ACCESS_PATH] = self.storage_ip
        if state:
            param_map[SMF_KEY_ENABLE_TIER] = 'true'
        else:
            param_map[SMF_KEY_ENABLE_TIER] = 'false'
        (status, response_map) = self.server.send_request(
            HttpMethod.PUT.value, URI_MOD_LDISK.format(ldisk), param_map)
        if status == HttpCode.OK.value:
            logger.info(
                'Modify tiering of LDISK {} successfully'.format(ldisk))
            return True
        else:
            logger.info('Modify tiering of LDISK {} failed. Error message: {}'.format(ldisk,
                                                                                      response_map[SMF_KEY_ERROR_DESCRIPTION]))
            return False

    def get_all_ldisk_enable_tier(self):
        (status, response_map) = self.server.send_request(
            HttpMethod.GET.value, URI_GET_TIERING.format(self.storage_ip))
        if status == HttpCode.OK.value:
            pool_maps = response_map[SMF_KEY_POOL_LIST]
            for pool_map in pool_maps:
                tier_maps = pool_map[SMF_KEY_TIER_LIST]
                for tier_map in tier_maps:
                    if tier_map[SMF_KEY_TIERING_FUNCTION] == 'enable':
                        yield int(tier_map[SMF_KEY_VOLUME_I_D])
        else:
            logger.info('Get all cache failed. Error message: {}'.format(
                response_map[SMF_KEY_ERROR_DESCRIPTION]))
            return False

    def __get_base_ldisk(self, ldisk):
        (status, response_map) = self.server.send_request(
            HttpMethod.GET.value, URI_GET_SNAPSHOT_BY_ID.format(ldisk, self.storage_ip))
        if status == HttpCode.OK.value:
            snap_map = response_map[SMF_KEY_SNAPSHOTS][0]
            base_ldisk_map = snap_map[SMF_KEY_BASE_VOLUME]
            return int(base_ldisk_map[SMF_KEY_DEVICE_ID])
        else:
            logger.info('Get base ldisk failed. Error message: {}'.format(
                response_map[SMF_KEY_ERROR_DESCRIPTION]))
            return -1

    def __change_current_ldisk(self, ldisk, operation):
        param_map = {}
        param_map[SMF_KEY_ACCESS_PATH] = self.storage_ip
        param_map[SMF_KEY_OPERATION] = operation
        (status, response_map) = self.server.send_request(
            HttpMethod.PUT.value, URI_MOD_SNAPSHOT.format(ldisk), param_map)
        if status == HttpCode.ACCEPTED.value:
            logger.info('Modify snapshot {} successfully'.format(ldisk))
            return True
        else:
            logger.info('Modify snapshot {}. Error message: {}'.format(ldisk,
                                                                       response_map[SMF_KEY_ERROR_DESCRIPTION]))
            return False
