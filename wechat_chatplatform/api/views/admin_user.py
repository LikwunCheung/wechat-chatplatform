# -*- coding: utf-8 -*-

import ujson

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse

from wechat_chatplatform.platform_admin.models import AdminUser
from wechat_chatplatform.common.choices import AdminUserStatus
from wechat_chatplatform.common.utils.utils import init_http_bad_request, make_json_response
from wechat_chatplatform.common.config import DOMAIN, ADMIN_INDEX, LOGIN_REDIRECT


def admin_user_login(request):
    param = ujson.loads(request.body)
    print(param)
    if request.method == 'POST':
        param = ujson.loads(request.body)
        username = param.get(r'username', None)
        password = param.get(r'password', None)
        print(password, username)

        try:
            # admin_user = AdminUser.objects.get(status=AdminUserStatus.active.value, username=username, password=password)
            request.session['username'] = username
            # request.session['type'] = admin_user.type_id.tag
            request.session['is_admin'] = True
            request.session['is_anchor'] = False
            request.session['is_user'] = False
            request.session['is_login'] = True
            request.session.set_expiry(15 * 60)
        except Exception as e:
            resp = init_http_bad_request('Error Username Or Password')
            return make_json_response(HttpResponseBadRequest, resp)

        redirect = param.get('redirect', None)
        if redirect:
            return HttpResponseRedirect(redirect)
        print(ADMIN_INDEX)
        return HttpResponseRedirect(DOMAIN + ADMIN_INDEX)
    print(LOGIN_REDIRECT)
    return HttpResponseRedirect(DOMAIN + ADMIN_INDEX)


def admin_user_logout(request):
    pass
