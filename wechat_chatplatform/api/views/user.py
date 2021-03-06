# -*- coding: utf-8 -*-

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, HttpResponseBadRequest

from wechat_chatplatform.user_info.models import UserInfo
from wechat_chatplatform.common.choices import AdminUserStatus
from wechat_chatplatform.common.utils.utils import init_http_bad_request, make_json_response
from wechat_chatplatform.common.config import DOMAIN, ADMIN_INDEX, LOGIN_REDIRECT


def user_login(request):

    admin_user = AdminUser.objects.filter(status=AdminUserStatus.active.value, username=username, password=password)
    if admin_user:
        request.session['username'] = username
        request.session['type'] = admin_user.type_id.tag
        request.session['is_admin'] = True
        request.session['is_anchor'] = False
        request.session['is_user'] = False
        request.session['is_login'] = True
        request.session.set_expiry(15 * 60)
    else:
        resp = init_http_bad_request('Error Username Or Password')
        make_json_response(HttpResponseBadRequest, resp)

    redirect = request.GET.get('redirect', '')
    if redirect:
        return HttpResponseRedirect(redirect)
    return HttpResponseRedirect(DOMAIN + ADMIN_INDEX)