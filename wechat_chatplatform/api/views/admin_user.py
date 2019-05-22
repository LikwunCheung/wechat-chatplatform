# -*- coding: utf-8 -*-

import ujson
import uuid

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse

from wechat_chatplatform.platform_admin.models import AdminUser
from wechat_chatplatform.common.choices import AdminUserStatus
from wechat_chatplatform.common.utils.utils import init_http_bad_request, make_json_response, init_http_success
from wechat_chatplatform.common.config import DOMAIN, ADMIN_INDEX, LOGIN_REDIRECT


def admin_user_login(request):

    if request.method == 'POST':
        param = ujson.loads(request.body)
        username = param.get('user_name', None)
        password = param.get('password', None)

        try:
            admin_user = AdminUser.objects.get(status=AdminUserStatus.active.value, username=username, password=password)

            request.session['username'] = username
            request.session['type'] = admin_user.admin_user_type.tag
            request.session['is_admin'] = True
            request.session['is_anchor'] = False
            request.session['is_user'] = False
            request.session['is_login'] = True
            request.session.set_expiry(15 * 60)
        except Exception as e:
            resp = init_http_bad_request('Error Username Or Password')
            return make_json_response(HttpResponseBadRequest, resp)

        # redirect = param.get('redirect', None)
        return HttpResponse(ujson.dumps(dict(data=dict(token=uuid.uuid1().__str__()))), content_type='application/json')

    return HttpResponseBadRequest()


def admin_user_logout(request):
    if request.method == 'POST':
        if request.session.get('username', None):
            request.session.clear()
    return HttpResponse()


def admin_user_logout(request):
    pass


def get_user_info(request):
    username = request.session.get('username', None)

    if not username:
        resp = init_http_bad_request()
        return make_json_response(HttpResponseBadRequest, resp)

    admin_user = AdminUser.objects.get(status=AdminUserStatus.active.value, username=username)

    resp = init_http_success()
    resp['data'] = dict(
        nickname=admin_user.nickname,
        avatar=''
    )

    return make_json_response(HttpResponse, resp)


