# -*- coding: utf-8 -*-

from .base_setting import *

# SECRET_KEY = 'w-l*xefx)8+p_1yu^8)mk6df(pushufs(hp6!hyx)a$u4o@*kz'

DEBUG = True

ALLOWED_HOSTS = ['*']

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, '../../db.sqlite3'),
    # },
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'suave',
        'USER': 'lihuan',
        'PASSWORD': 'lihuan',
        'HOST': '47.74.66.156',
        'PORT': 8088,
        'CHARSET': 'utf8mb4'
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