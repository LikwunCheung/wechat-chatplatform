# -*- coding: utf-8 -*-

from enum import Enum


class ErrorCode(Enum):
    success = 0
    not_found = 1
    unauthorized = 2
    bad_request = 3


class ErrorMsg(Enum):
    success = 'success'
    not_found = 'resource not found'
    unauthorized = 'unauthorized access'
    bad_request = 'bad request'


HTTP_X_API_KEY = 'HTTP_X_API_KEY'
API_KEY = '227415ba68c811e9b1a48c8590c7151e'
DOMAIN = 'http://www.suavechat.com/'
LOGIN_REDIRECT = 'admin/login/'

