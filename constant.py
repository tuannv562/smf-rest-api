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
SMF_KEY_VOLUME_IDS = 'volumeIds'
SMF_KEY_TOSHIBA_CACHE_TYPE = 'toshibaCacheType'
SMF_KEY_CACHE_TYPE='cacheType'


MSG_CREATING_LDISK = ' Processing the volume definition'