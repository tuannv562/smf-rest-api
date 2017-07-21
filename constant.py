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
URI_MOD_UNASSIGN_CACHE = '/smf_api/cachepartition/volumes'
URI_DEL_CACHE = '/smf_api/cachepartition/?accesspath={}&inelements=%7B{}%7D'
URI_GET_TIERING = '/smf_api/tiers/detail/?accesspath={}'
URI_GET_SNAPSHOT_BY_ID = '/smf_api/replications/snapshots/{}?accesspath={}'
URI_MOD_SNAPSHOT = '/smf_api/replications/snapshots/{}'

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
SMF_KEY_VOLUME_I_D = 'volume_id'
SMF_KEY_VOLUME_IDS = 'volumeIds'
SMF_KEY_TOSHIBA_CACHE_TYPE = 'toshibaCacheType'
SMF_KEY_CACHE_TYPE = 'cacheType'
SMF_KEY_POOL_LIST = 'poolList'
SMF_KEY_TIER_LIST = 'tierList'
SMF_KEY_TIERING_FUNCTION = 'toshibaTieringFunction'
SMF_KEY_SNAPSHOTS = 'snapShots'
SMF_KEY_BASE_VOLUME = 'toshibaBaseVolume'
SMF_KEY_OPERATION = 'operation'


MSG_CREATING_LDISK = ' Processing the volume definition'
MSG_DEL_LDISK_TIERING_ENABLE = ' can not delete the volume because tiering function in the volume is enabled'
MSG_HAS_LDISK_ENABLE_TIER = ' the partition for tiering can not be deleted because volume that tiering is enabled exists'
MSG_DEL_LDISK_HAS_SNAPSHOT = ' There are snapshot volumes belonging to the volume'
MSG_DEL_SNAPSHOT_LDISK = ' The volume is set to snapshot mode'
