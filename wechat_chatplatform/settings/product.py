# -*- coding: utf-8 -*-

from .base_setting import *

# SECRET_KEY = 'w-l*xefx)8+p_1yu^8)mk6df(pushufs(hp6!hyx)a$u4o@*kz'

DEBUG = True

ALLOWED_HOSTS = ['47.74.66.156', 'www.suavechat.com']

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_COOKIE_NAME = "sessionid"

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
            'format': '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d][%(levelname)s][%(message)s]'
        },
        'simple': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
        },
        'collect': {
            'format': '%(message)s'
        }
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/root/logs/default.log',
            'maxBytes': 1024 * 1024 * 50,
            'formatter': 'simple',
            'encoding': 'utf-8',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/root/logs/error.log',
            'maxBytes': 1024 * 1024 * 50,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'collect': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/root/logs/collect.log',
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 1,
            'formatter': 'collect',
            'encoding': "utf-8"
        },
    },
    'loggers': {
        'django': {
            'handlers': ['default', 'console', 'error'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'collect': {
            'handlers': ['console', 'collect'],
            'level': 'INFO',
        },
    }
}

