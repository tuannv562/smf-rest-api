from enum import Enum
LOG_SETTING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(module)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler'
        },
        'file': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'smf-rest-api.log',
            'maxBytes': 10485760,
            'backupCount': 10,
            'encoding': 'utf8'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True
        },
    }
}


class HttpCode(Enum):
    OK = 200
    Created = 201
    Accepted = 202
    InternalServerError = 500
