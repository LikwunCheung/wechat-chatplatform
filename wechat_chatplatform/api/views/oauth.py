# -*- coding: utf-8 -*-

import ujson
import base64
import logging
from datetime import datetime

from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods

from wechat_chatplatform.user_info.models import UserInfo, UserLoginInfo
from wechat_chatplatform.anchor.models import Anchor
from wechat_chatplatform.common.utils.utils import *
from wechat_chatplatform.handler.wechat_handler.wechat_handler import wechat_handler

logger = logging.getLogger('django')


@require_http_methods(['GET', 'OPTIONS'])
def oauth_router(request):
    if request.method == 'GET':
        return oauth_get_code(request)
    return HttpResponseNotAllowed()


def oauth_get_code(request):
    code = request.GET.get('code', None)
    state = request.GET.get('state', None)
    if not code:
        resp = init_http_bad_request('No Open ID')
        return make_json_response(HttpResponseBadRequest, resp)

    open_id, access_token = wechat_handler.get_user_open_id_access_token(code)

    try:
        anchor = Anchor.objects.get(open_id=open_id)
        anchor_login(request, anchor)
        return HttpResponseRedirect(DOMAIN + state)
    except Exception as e:
        pass

    try:
        user = UserInfo.objects.get(open_id=open_id)
        user.last_login = now()
        user.save()
    except Exception as e:
        userinfo = wechat_handler.get_user_info(open_id, access_token)
        params = dict(
            open_id=open_id,
            access_token=access_token,
            avatar=userinfo['headimgurl'],
            gender=0 if userinfo['sex'] == 2 else 1,
            last_login=now()
        )
        user = UserInfo(**params)
        user.save_nickname(userinfo['nickname'])
        user.save()

    user_record = UserLoginInfo(user=user, time=now())
    user_record.save()
    user_login(request, user)
    logger.warning('User Login: %s/%s' % (request.META['HTTP_HOST'], request.path))
    res = HttpResponseRedirect(DOMAIN + state)
    return res


def anchor_login(request, anchor):
    request.session['id'] = anchor.anchor_id
    request.session['type'] = anchor.anchor_type.anchor_type_id
    request.session['is_admin'] = False
    request.session['is_anchor'] = True
    request.session['is_user'] = False
    request.session['is_login'] = True
    request.session.set_expiry(60 * 60)
    logger.info('Anchor Login: %s' % anchor.anchor_id)


def user_login(request, user):
    request.session['id'] = user.user_id
    request.session['is_admin'] = False
    request.session['is_anchor'] = False
    request.session['is_user'] = True
    request.session['is_login'] = True
    request.session.set_expiry(60 * 60)
    logger.info('User Login: %s' % user.user_id)
