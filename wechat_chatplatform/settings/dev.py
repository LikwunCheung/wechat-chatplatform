# -*- coding: utf-8 -*-

from .base_setting import *

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../../db.sqlite3'),
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'
        },
        'debug': {
            'format': '%(asctime)s [%(module)s:%(funcName)s][%(levelname)s] %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'debug.console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'debug',
        },
        # 'default': {
        #     'level': 'DEBUG',
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'filename': '/home/ubuntu/log/all.log',
        #     'maxBytes': 1024*1024*5,
        #     'backupCount': 5,
        #     'formatter': 'debug',
        # },
        # 'error': {
        #     'level': 'ERROR',
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'filename': '/home/ubuntu/log/error.log',
        #     'maxBytes': 1024 * 1024 * 5,
        #     'backupCount': 5,
        #     'formatter': 'debug',
        # },
    },
    'loggers': {
        'django.debug': {
            'handlers': ['debug.console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        # 'server.debug': {
        #     'handlers': ['default', 'debug.console'],
        #     'propagate': True,
        #     'level': 'DEBUG',
        # },
    }
}