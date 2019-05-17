# -*- coding: utf-8 -*-

from .base_setting import *

DEBUG = True

ALLOWED_HOSTS = ['*']

ROOT_URLCONF = 'wechat_chatplatform.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../../db.sqlite3'),
    },
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'suave',
        'USER': 'lihuan',
        'PASSWORD': 'lihuan',
        'HOST': '115.146.85.81',
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