# -*- coding: utf-8 -*-

import ujson
import logging

from django.http.response import HttpResponseForbidden, HttpResponseBadRequest, HttpResponse, HttpResponseRedirect

from wechat_chatplatform.common.config import *

logger = logging.getLogger('django')


def make_dict(keys, kwargs):
    result = dict()
    for key in kwargs.keys():
        if key in keys:
            result.update({key: kwargs[key]})
    return result


def check_api_key(func):
    def wrapper(request, *args, **kwargs):
        api_key = request.META.get(HTTP_X_API_KEY, None)
        if api_key == API_KEY:
            return func(request, args, kwargs)
        else:
            logger.warning('Unpermitted Access To \'%s\'', request.path_info)
            resp = init_http_unauthorized('Unpermitted Access To \'%s\'' % request.path_info)
            return make_json_response(HttpResponseForbidden, resp)
    return wrapper


def check_user_login(func):
    def wrapper(request):
        user_id = request.session.get('id', '')
        login = request.session.get('isUser', False)
    pass


def check_admin_user(func):
    def wrapper(request, *args, **kwargs):
        username = request.session.get('username', None)
        is_admin = request.session.get('is_admin', False)
        is_login = request.session.get('is_login', False)

        if not (username and is_admin and is_login):
            resp = init_http_response(ErrorCode.admin_user_unlogin.value, ErrorMsg.admin_user_unlogin.value)
            return make_json_response(HttpResponse, resp)
        else:
            request.session.set_expiry(ADMIN_USER_SEESION)
            return func(request, args, kwargs)
    return wrapper


def make_json_response(func=HttpResponse, resp=None):
    return func(ujson.dumps(resp), content_type='application/json')


def make_redirect_response(func=HttpResponse, resp=None):
    return func(ujson.dumps(resp), content_type='application/json', status=302)


def init_http_response(err_code, err_msg):
    return dict(
        err_code=err_code,
        err_msg=err_msg,
        data=dict(),
    )


def init_redirect_response(url=None):
    return dict(url=url)


def init_http_success(err_msg=None):
    if not err_msg:
        return init_http_response(ErrorCode.success.value, ErrorMsg.success.value)
    return init_http_response(ErrorCode.success.value, err_msg)


def init_http_not_found(err_msg=None):
    if not err_msg:
        return init_http_response(ErrorCode.not_found.value, ErrorMsg.not_found.value)
    return init_http_response(ErrorCode.not_found.value, err_msg)


def init_http_bad_request(err_msg=None):
    if not err_msg:
        return init_http_response(ErrorCode.bad_request.value, ErrorMsg.not_found.value)
    return init_http_response(ErrorCode.bad_request.value, err_msg)


def init_http_unauthorized(err_msg=None):
    if not err_msg:
        return init_http_response(ErrorCode.unauthorized.value, ErrorMsg.unauthorized.value)
    return init_http_response(ErrorCode.unauthorized.value, err_msg)


if __name__ == '__main__':

    def test_make_dict(keys, **kwargs):
        return make_dict(keys=keys, kwargs=kwargs)

    keys = ['a', 'c']
    print(test_make_dict(keys=keys, a=1, b=2, c=3, d=4))
