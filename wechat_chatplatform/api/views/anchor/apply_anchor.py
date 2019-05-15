# -*- coding: utf-8 -*-

import ujson
from datetime import datetime

from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods
from django.utils.timezone import now

from wechat_chatplatform.anchor.models import Anchor, AnchorType, AnchorApplyRecord
from wechat_chatplatform.common.utils.utils import *
from wechat_chatplatform.common.config import *
from wechat_chatplatform.common.choices import *
from wechat_chatplatform.handler.anchor_apply_record_handler import anchor_apply_record_handler
from wechat_chatplatform.common.utils.dingtalk_robot_utils import send_new_applier_message


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
    keys = ['nickname', 'city', 'birthday', 'gender', 'wechat_id', 'audio', 'avatar', 'image', 'slogan', 'tags',
            'skill', 'experience', 'occupation', 'online']

    param = ujson.loads(request.body)
    print(param)

    try:
        param['tags'] = ','.join([str(tag).strip('#') for tag in param['tags']])
        param['image'] = param['image'][0:3] if len(param['image']) > 3 else param['image']
        param['image'] = ','.join(param['image'])
    except Exception as e:
        print(e)
        resp = init_http_bad_request('AttributeError')
        return make_json_response(HttpResponseBadRequest, resp)

    anchor = anchor_apply_record_handler.apply_anchor(param)
    if not anchor:
        resp = init_http_bad_request('Some Error Happend')
        return make_json_response(HttpResponseBadRequest, resp)

    send_new_applier_message(anchor)
    resp = init_http_success()
    return make_json_response(HttpResponse, resp)


def anchor_apply_unaudit_get(request):
    anchor_apply_records = AnchorApplyRecord.objects.filter(status=AnchorAuditStatus.unaudit.value)
    results = []

    for anchor_apply_record in anchor_apply_records:
        results.append(dict(
            id=anchor_apply_record.record_id,
            nickname=anchor_apply_record.nickname,
            city=anchor_apply_record.city,
            birthday=anchor_apply_record.birthday.strftime('%Y-%m-%d'),
            gender=dict(Gender.GenderChoices.value)[anchor_apply_record.gender],
            wechat_id=anchor_apply_record.wechat_id,
            audio=anchor_apply_record.audio,
            image=anchor_apply_record.image.split(','),
            slogan=anchor_apply_record.slogan,
            tags=anchor_apply_record.tags.split(','),
            experience=anchor_apply_record.experience,
            online=anchor_apply_record.online,
            occupation=anchor_apply_record.occupation,
            skill=anchor_apply_record.skill,
            apply_date=anchor_apply_record.apply_date.strftime('%Y-%m-%d %H:%m:%S'),
        )
        )

    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)


def anchor_apply_action_post(request, action):
    param = ujson.loads(request.body)
    anchor_apply_reocrd_id = param.get('id', None)

    if not anchor_apply_reocrd_id:
        resp = init_http_bad_request('No Apply Record ID')
        return make_json_response(HttpResponseBadRequest, resp)

    try:
        anchor_apply_record = AnchorApplyRecord.objects.get(record_id=anchor_apply_reocrd_id)
    except Exception as e:
        resp = init_http_bad_request('No Match Apply Record')
        return make_json_response(HttpResponseBadRequest, resp)

    if anchor_apply_record.status != AnchorAuditStatus.unaudit.value:
        resp = init_http_bad_request('Anchor Had Been Audited')
        return make_json_response(HttpResponseBadRequest, resp)

    if action == 'pass':
        level = param.get('level', 1)

        type = AnchorType.objects.get(type_id=level)
        anchor_apply_record.audit_pass(None, type)
    elif action == 'reject':
        anchor_apply_record.audit_fail(None)

    results = dict(
        id=anchor_apply_record.record_id,
        name=anchor_apply_record.nickname,
        status=dict(AnchorAuditStatus.AnchorAuditStatusChoice.value)[anchor_apply_record.status]
    )
    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)
