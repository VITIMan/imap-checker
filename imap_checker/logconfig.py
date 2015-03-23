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
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'filename': '/tmp/imap_checker.log',
            'mode': 'a',
            'maxBytes': 10485760,
            'backupCount': 5,
        },
    },
    # 'loggers': {
    #     'dev': {
    #         'level': 'DEBUG',
    #         'handlers': ['console'],
    #     },
    #     'to_file': {
    #         'level': 'DEBUG',
    #         'handlers': ['file'],
    #     },
    # },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
    }
}
