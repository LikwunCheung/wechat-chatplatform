# -*- coding: utf-8 -*-

from enum import Enum


class ErrorCode(Enum):
    success = 0
    not_found = 1
    unauthorized = 2
    bad_request = 3
    not_super_admin = 6
    admin_user_unlogin = 7


class ErrorMsg(Enum):
    success = 'success'
    not_found = 'resource not found'
    unauthorized = 'unauthorized access'
    bad_request = 'bad request'
    not_super_admin = 'not super admin user'
    admin_user_unlogin = 'admin user unlogin'


HTTP_X_API_KEY = 'HTTP_X_API_KEY'
API_KEY = '227415ba68c811e9b1a48c8590c7151e'
DOMAIN = 'http://www.suavechat.com/'
ORDER_PAGE = '#/order'
LOGIN_REDIRECT = 'admin/'
ACCEPT_ORDER = 'api/v1/order/accept/?id={}'
GRAB_ORDER = 'api/v1/order/random/accept/?id={}&anchor_id={}'
ADMIN_INDEX = 'admin/#/manage'

MYSQL_COMMAND = 'sudo docker run --name mysql --restart always  --privileged=true -e MYSQL_USER="lihuan" ' \
                '-e MYSQL_PASSWORD="lihuan" -e MYSQL_ROOT_PASSWORD="lihuan" -v=/mnt/mysql/log/:/var/log/mysql/ ' \
                '-v=/mnt/mysql/data:/var/lib/mysql -p 8088:3306 -d mysql --character-set-server=utf8mb4 ' \
                '--collation-server=utf8mb4_general_ci --default-authentication-plugin=mysql_native_password'

ADMIN_USER_SEESION = 1 * 60
