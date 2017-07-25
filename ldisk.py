from storage_attribute import StorageAttribute
import logging
import logging.config
from config import LOG_SETTING, HttpCode, HttpMethod
from server import Server
from constant import *
import time

logger = logging.getLogger(__name__)
logging.config.dictConfig(LOG_SETTING)


class Ldisk(StorageAttribute):
    def __init__(self, server: Server, storage_ip, lower, upper):
        if not lower:
            lower = 0
        if not upper:
            upper = 2047
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
        snapshots = list(self.__get_snapshot_ldisks())
        print('Snapshot LDISK {}'.format(snapshots))
        for i in snapshots:
            if i >= self.lower and i <= self.upper:
                self.__remove_snapshot(i)
                ldisks.remove(i)
        for i in ldisks:
            self.__remove_ldisk(i)

    def __get_all_ldisk(self):
        (status, content_map) = self.server.send_request(
            HttpMethod.GET.value, URI_GET_ALL_VOLUMES.format(self.storage_ip))
        volumes_map = content_map[SMF_KEY_VOLUMES]
        for volume_map in volumes_map:
            yield int(volume_map[SMF_KEY_DEVICE_ID])

    def __remove_ldisk(self, ldisk):
        result, message = self.server.send_sync_request(HttpMethod.DELETE.value, URI_DEL_LDISK.format(
            ldisk, self.storage_ip), {}, HttpCode.OK.value, MSG_DELETING_LDISK)
        if result:
            print('Delete LDISK {} successfully'.format(ldisk))
            return True
        else:
            if message == MSG_DEL_LDISK_TIERING_ENABLE:
                # ldisk enable tiering
                ldisks_enable_tier = list(self.get_all_ldisk_enable_tier())
                for i in ldisks_enable_tier:
                    self.set_tiering_of_ldisk(i, False)
                self.__remove_ldisk(ldisk)
            elif message == MSG_DEL_LDISK_HAS_SNAPSHOT:
                snapshots = list(self.__get_all_snapshot_of_ldisk(ldisk))
                for snapshot in snapshots:
                    self.__remove_snapshot(snapshot)
                self.__remove_ldisk(ldisk)
            elif 'Sense key' in message:
                print('waitting 10s')
                time.sleep(10)
                self.__remove_ldisk(ldisk)
            elif message == MSG_MIRROR_SET_EXIST or message == MSG_REMOTE_MIRROR_SET_EXIST:
                self.__remove_mirror(ldisk)
                self.__remove_ldisk(ldisk)
            else:
                logger.info('Delete LDISK {} failed. Error message: {}'.format(
                    ldisk, message))
                print('Delete LDISK {} failed. Error message: {}'.format(
                    ldisk, message))
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
        (_, response_map) = self.server.send_request(
            HttpMethod.GET.value, URI_GET_TIERING.format(self.storage_ip))
        pool_maps = response_map[SMF_KEY_POOL_LIST]
        for pool_map in pool_maps:
            tier_maps = pool_map[SMF_KEY_TIER_LIST]
            for tier_map in tier_maps:
                if tier_map[SMF_KEY_TIERING_FUNCTION] == 'enable':
                    yield int(tier_map[SMF_KEY_VOLUME_I_D])

    def __get_snapshot_ldisks(self):
        (status, response_map) = self.server.send_request(
            HttpMethod.GET.value, URI_GET_SNAPSHOT.format(self.storage_ip))
        snapshot_maps = response_map[SMF_KEY_SNAPSHOTS]
        for snapshot_map in snapshot_maps:
            synced_map = snapshot_map[SMF_KEY_SYNCED_ELEMENT]
            yield int(synced_map[SMF_KEY_DEVICE_ID])

    def __get_snapshot_info_of_ldisk(self, ldisk):
        (_, response_map) = self.server.send_request(
            HttpMethod.GET.value, URI_GET_SNAPSHOT_BY_ID.format(ldisk, self.storage_ip))
        snap_map = response_map[SMF_KEY_SNAPSHOTS][0]
        base_ldisk_map = snap_map[SMF_KEY_BASE_VOLUME]
        current_ldisk_map = snap_map[SMF_KEY_CURRENT_VOLUME]
        return (int(base_ldisk_map[SMF_KEY_DEVICE_ID]), int(current_ldisk_map[SMF_KEY_DEVICE_ID]))

    def __modify_snapshot(self, ldisk, operation):
        param_map = {
            SMF_KEY_ACCESS_PATH: self.storage_ip,
            SMF_KEY_OPERATION: operation
        }
        (status, response_map) = self.server.send_request(
            HttpMethod.PUT.value, URI_MOD_SNAPSHOT.format(ldisk), param_map)
        if status == HttpCode.ACCEPTED.value:
            logger.info('Modify snapshot {} successfully'.format(ldisk))
            return True
        else:
            logger.info('Modify snapshot {}. Error message: {}'.format(ldisk,
                                                                       response_map[SMF_KEY_ERROR_DESCRIPTION]))
            return False

    def __get_all_snapshot_of_ldisk(self, ldisk):
        _, response_map = self.server.send_request(
            HttpMethod.GET.value, URI_GET_SNAPSHOT.format(self.storage_ip))
        snapshot_maps = response_map[SMF_KEY_SNAPSHOTS]
        for snapshot_map in snapshot_maps:
            base_map = snapshot_map[SMF_KEY_BASE_VOLUME]
            if int(base_map[SMF_KEY_DEVICE_ID]) == ldisk:
                synced_map = snapshot_map[SMF_KEY_SYNCED_ELEMENT]
                yield int(synced_map[SMF_KEY_DEVICE_ID])

    def __remove_snapshot(self, snapshot):
        base, current = self.__get_snapshot_info_of_ldisk(snapshot)
        if base != current:
            self.__modify_snapshot(base, 'change')
        result, message = self.server.send_sync_request(HttpMethod.DELETE.value, URI_DEL_SNAPSHOT.format(
            snapshot, self.storage_ip), {}, HttpCode.OK.value, MSG_DELETING_LDISK)
        if result:
            print('Delete snapshot {} successfully'.format(snapshot))
            return True
        else:
            logger.info('Remove snapshot {}. Error message: {}'.format(
                snapshot, message))
            print('Remove snapshot {} failed. Error message: {}'.format(
                snapshot, message))
            return False

    def __get_mirror_mode_of_ldisk(self, ldisk):
        _, response_map = self.server.send_request(
            HttpMethod.GET.value, URI_GET_MIRROR_DETAIL.format(self.storage_ip))
        mirror_maps = response_map[SMF_KEY_SYNCHRONIZATIONS]
        for mirror_map in mirror_maps:
            system_map = mirror_map[SMF_KEY_SYSTEM_ELEMENT]
            system = int(system_map[SMF_KEY_DEVICE_ID])
            synced_map = mirror_map[SMF_KEY_SYNCED_ELEMENT]
            synced = int(synced_map[SMF_KEY_DEVICE_ID])
            if system == ldisk or synced == ldisk:
                if SMF_KEY_MODE in mirror_map:
                    return 'local'
                else:
                    return 'remote'

    def __split_mirror(self, ldisk, mode):
        param_map = {
            SMF_KEY_ACCESS_PATH: self.storage_ip,
            SMF_KEY_OPERATION: 'split',
            SMF_KEY_MODE: mode,
            SMF_KEY_FORCE: 'true'
        }
        status, response_map = self.server.send_request(
            HttpMethod.PUT.value, URI_SPLIT_MIRROR.format(ldisk))
        if status == HttpCode.ACCEPTED.value:
            logger.info(
                'Split mirror set of LDISK {} successfully'.format(ldisk))
        else:
            logger.info('Split mirror set of LDISK {} failed. Error message: {}'.format(
                ldisk, response_map[SMF_KEY_ERROR_DESCRIPTION]))

    def __remove_mirror(self, ldisk):
        mode = self.__get_mirror_mode_of_ldisk(ldisk)
        self.__split_mirror(ldisk, mode)
        status, response_map = self.server.send_request(
            HttpMethod.DELETE.value, URI_DEL_MIRROR.format(ldisk, self.storage_ip, mode))
        if status == HttpCode.OK.value:
            logger.info(
                'Delete mirror set LDISK {} successfully.'.format(ldisk))
        else:
            logger.info('Delete mirror set LDISK {} failed. Error message: {}.'.format(
                ldisk, response_map[SMF_KEY_ERROR_DESCRIPTION]))
