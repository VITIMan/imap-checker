# -*- coding: utf-8 -*-

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    }
}
