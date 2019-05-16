# -*- coding: utf-8 -*-

import ujson
from datetime import datetime

from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods

from wechat_chatplatform.user_info.models import UserInfo, UserLoginInfo
from wechat_chatplatform.common.utils.utils import *
from wechat_chatplatform.handler.wechat_handler.wechat_handler import wechat_handler


@require_http_methods(['GET', 'OPTIONS'])
def oauth_router(request):
    if request.method == 'GET':
        return oauth_get_code(request)
    return HttpResponseNotAllowed()


def oauth_get_code(request):
    code = request.GET.get('code', None)
    if not code:
        resp = init_http_bad_request('No Open ID')
        return make_json_response(HttpResponseBadRequest, resp)

    open_id, access_token = wechat_handler.get_user_open_id_access_token(code)

    try:
        user = UserInfo.objects.get(open_id=open_id)
        user.last_login = now()
    except Exception as e:
        userinfo = wechat_handler.get_user_info(open_id, access_token)
        params = dict(
            open_id=open_id,
            access_token=access_token,
            nickname=userinfo['nickname'],
            avatar=userinfo['headimgurl'],
            gender=0 if userinfo['sex'] == 2 else 1,
            last_login=now()
        )
        user = UserInfo(**params)
        user.save()

    user_record = UserLoginInfo(user_id=user, time=now())
    user_record.save()

    return HttpResponseRedirect('http://www.suavechat.com/')


