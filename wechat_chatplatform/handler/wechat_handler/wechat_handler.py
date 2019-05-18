# -*- coding: utf-8 -*-

import ujson
import requests
import time
import urllib.parse

from .config import *


class AccessTokenError(BaseException):

    def __init__(self, ErrorInfo=None):
        super().__init__(self)
        self.error_info = ErrorInfo

    def __str__(self):
        return self.error_info


class WeChatHandler(object):

    def __init__(self):
        self.access_token = None
        self.access_token_time = 0
        self.access_token_expire = 0

    def renew_access_token(self):
        params = dict(
            grant_type=ACCESS_TOKEN_GRANT_TYPE,
            appid=APP_ID,
            secret=APP_SECRET
        )
        resp = requests.get(ACCESS_TOKEN_URL, params=params)
        resp = ujson.loads(resp.content)
        if 'errcode' in resp:
            self.access_token = None
            return
        self.access_token = resp['access_token']
        self.access_token_expire = resp['expires_in']
        self.access_token_time = time.time()

    def get_access_token(self):
        if (time.time() - self.access_token_time) >= (self.access_token_expire - 60):
            self.renew_access_token()
            if not self.access_token:
                raise AccessTokenError('Wechat Server Connect Error')
        return self.access_token

    def get_code_url(self, state=None):
        params = dict(
            appid=APP_ID,
            redirect_uri=USER_CODE_REDIRECT_URL,
            response_type=USER_CODE_RESPONSE_TYPE,
            scope=USER_CODE_SCOPE,
            state=state,
            connect_redirect=1
        )
        url = USER_CODE_URL + '?' + urllib.parse.urlencode(params) + USER_CODE_WECHAT
        return url

    def get_user_open_id_access_token(self, code):
        params = dict(
            appid=APP_ID,
            secret=APP_SECRET,
            code=code,
            grant_type=USER_TOKEN_GRANT_TYPE
        )
        resp = requests.get(USER_TOKEN_URL, params=params)
        resp = ujson.loads(resp.content)
        openid = resp['openid']
        access_token = resp['access_token']
        return openid, access_token

    def get_user_info(self, openid, access_token):
        params = dict(
            access_token=access_token,
            openid=openid,
            lang=USER_INFO_LANG
        )
        resp = requests.get(USER_INFO_URL, params=params)
        resp = ujson.loads(resp.content)
        return resp


wechat_handler = WeChatHandler()


if __name__ == '__main__':
    pass
    # print(wechat_handler.get_access_token())