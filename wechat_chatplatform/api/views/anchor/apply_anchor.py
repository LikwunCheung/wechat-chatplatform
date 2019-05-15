# -*- coding: utf-8 -*-

import ujson
from datetime import datetime

from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods
from django.utils.timezone import now

from wechat_chatplatform.anchor.models import Anchor, AnchorType, AnchorGroup, AnchorCity, AnchorTag
from wechat_chatplatform.common.utils.utils import *
from wechat_chatplatform.common.config import *
from wechat_chatplatform.common.choices import *
from wechat_chatplatform.handler.anchor_handler import AnchorHandler
from wechat_chatplatform.common.utils.dingtalk_robot_utils import send_new_applier_message


anchor_handler = AnchorHandler()


@require_http_methods(['POST', 'OPTIONS'])
@check_api_key
def anchor_apply_router(requset, *args, **kwargs):
    if requset.method == 'POST':
        return anchor_apply_post(requset)
    return HttpResponseNotAllowed()


@require_http_methods(['GET', 'OPTIONS'])
@check_api_key
def anchor_apply_unaudit_router(requset, *args, **kwargs):
    if requset.method == 'GET':
        return anchor_apply_unaudit_get(requset)
    return HttpResponseNotAllowed()


@require_http_methods(['POST', 'OPTIONS'])
@check_api_key
def anchor_apply_action_router(requset, *args, **kwargs):
    action = None
    for arg in args:
        if isinstance(arg, dict):
            action = arg.get('action', None)
    if requset.method == 'POST':
        return anchor_apply_action_post(requset, action)
    return HttpResponseNotAllowed()


@require_http_methods(['GET', 'OPTIONS'])
@check_api_key
def anchor_apply_dingtalk_action_router(requset, *args, **kwargs):
    action = None
    for arg in args:
        if isinstance(arg, dict):
            action = arg.get('action', None)

    if requset.method == 'POST':
        return anchor_apply_action_post(requset, action)
    return HttpResponseNotAllowed()


def anchor_apply_post(request):
    keys = ['name', 'nickname', 'city_id', 'identity_type', 'identity', 'birthday', 'gender', 'mobile', 'wechat_id',
            'audio', 'avatar', 'image', 'slogan', 'tags']

    param = ujson.loads(request.body)
    print(param)

    try:
        param['tags'] = ','.join([str(tag) for tag in param['tags']])
        param['city_id'] = AnchorCity.objects.get(city_id=int(param['city_id']))
        param['identity_type'] = IdentityType.identity.value
        param['image'] = param['image'][0:3] if len(param['image']) > 3 else param['image']
        param['image'] = ','.join(param['image'])
    except Exception as e:
        print(e)
        resp = init_http_bad_request('AttributeError')
        return make_json_response(HttpResponseBadRequest, resp)

    param.update(dict(
        status=AnchorStatus.unaudit.value
    ))

    anchor = anchor_handler.apply_anchor(param)
    if not anchor:
        resp = init_http_bad_request('Some Error Happend')
        return make_json_response(HttpResponseBadRequest, resp)

    send_new_applier_message(anchor)
    resp = init_http_success()
    return make_json_response(HttpResponse, resp)


def anchor_apply_unaudit_get(request):

    anchors = Anchor.objects.filter(status=AnchorStatus.unaudit.value)
    results = []

    for anchor in anchors:
        results.append(dict(
                id=anchor.anchor_id,
                name=anchor.name,
                nickname=anchor.nickname,
                city=anchor.city_id.name,
                identity=anchor.identity,
                birthday=anchor.birthday.strftime('%Y-%m-%d'),
                gender=Gender.GenderChoices.value[anchor.gender][1],
                mobile=anchor.mobile,
                wechat_id=anchor.wechat_id,
                audio=anchor.audio,
                image=anchor.image.split(','),
                slogan=anchor.slogan,
                tags=anchor.tags.split(',')
            )
        )

    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)


def anchor_apply_action_post(request, action):
    param = ujson.loads(request.body)
    anchor_id = param.get('id', None)

    if not anchor_id:
        resp = init_http_bad_request('No Anchor ID')
        return make_json_response(HttpResponseBadRequest, resp)

    try:
        anchor = Anchor.objects.get(anchor_id=anchor_id)
    except Exception as e:
        resp = init_http_bad_request('No Match Anchor')
        return make_json_response(HttpResponseBadRequest, resp)

    if anchor.status != AnchorStatus.unaudit.value:
        resp = init_http_bad_request('Anchor Audited')
        return make_json_response(HttpResponseBadRequest, resp)

    if action == 'pass':
        level = request.POST.get('level', 1)
        anchor.type_id = AnchorType.objects.get(type_id=level)
        anchor.status = AnchorStatus.active.value
        anchor.join_date = now()
        anchor.audit_date = now()
        anchor.auditor = None
        anchor.save()
    elif action == 'reject':
        anchor.status = AnchorStatus.audit_fail.value
        anchor.audit_date = now()
        anchor.auditor = None
        anchor.save()

    results = dict(
        id=anchor.anchor_id,
        name=anchor.name,
        status=dict(AnchorStatus.AnchorStatusChoice.value)[anchor.status]
    )
    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)
