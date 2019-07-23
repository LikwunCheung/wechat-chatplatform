# -*- coding: utf-8 -*-

import ujson
from datetime import datetime
import logging

from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods
from django.utils.timezone import now
from django.contrib.sessions.models import Session

from wechat_chatplatform.anchor.models import AnchorType, AnchorApplyRecord
from wechat_chatplatform.platform_admin.models import AdminUser
from wechat_chatplatform.common.utils.utils import *
from wechat_chatplatform.user_info.models import UserInfo
from wechat_chatplatform.common.choices import *
from wechat_chatplatform.handler.anchor_apply_record_handler import anchor_apply_record_handler
from wechat_chatplatform.common.utils.dingtalk_robot_utils import send_new_applier_message, send_audit_pass_message, \
    send_audit_reject_message

logger = logging.getLogger('django')


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
    user_id = request.session.get('id', None)
    is_user = request.session.get('is_user', False)
    is_anchor = request.session.get('is_anchor', True)
    if not (user_id and is_user) or is_anchor:
        logger.warning('No Session User ID: %s' % request.get_full_path())
        return HttpResponseBadRequest()

    user = UserInfo.objects.get(user_id=user_id)
    param = ujson.loads(request.body)
    logger.warning(param)

    try:
        param['tags'] = ','.join([str(tag).strip('#') for tag in param['tags']])
        param['image'] = param['image'][0:3] if len(param['image']) > 3 else param['image']
        param['image'] = ','.join(param['image'])
        param['open_id'] = user.open_id
    except Exception as e:
        logger.error('Apply Anchor Error: %s' % e)
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
        tags = []
        if anchor_apply_record.tags:
            if ',' in anchor_apply_record.tags:
                tags = ['#' + tag for tag in anchor_apply_record.tags.split(',')]
            else:
                tags = '#' + anchor_apply_record.tags
        results.append(dict(
            id=anchor_apply_record.anchor_apply_record_id,
            nickname=anchor_apply_record.nickname,
            city=anchor_apply_record.city,
            birthday=anchor_apply_record.birthday.strftime('%Y-%m-%d'),
            gender=dict(Gender.GenderChoices.value)[anchor_apply_record.gender],
            wechat_id=anchor_apply_record.wechat_id,
            audio=anchor_apply_record.audio,
            image=anchor_apply_record.image.split(
                ',') if ',' in anchor_apply_record.image else [anchor_apply_record.image],
            slogan=anchor_apply_record.slogan,
            tags=tags,
            experience=anchor_apply_record.experience,
            online=anchor_apply_record.online,
            occupation=anchor_apply_record.occupation,
            skill=anchor_apply_record.skill,
            apply_date=anchor_apply_record.apply_date.strftime('%Y-%m-%d %H:%m:%S')
        ))
        results[-1]['image'].append(anchor_apply_record.avatar)

    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)


def anchor_apply_action_post(request, action):
    username = request.session.get('username', None)
    is_admin = request.session.get('is_admin', False)
    is_login = request.session.get('is_login', False)

    if not (username and is_admin and is_login):
        return HttpResponse(status=700)

    request.session.set_expiry(15 * 60)

    auditor = AdminUser.objects.get(username=username, status=AdminUserStatus.active.value)

    param = ujson.loads(request.body)
    anchor_apply_reocrd_id = param.get('id', None)

    if not anchor_apply_reocrd_id:
        resp = init_http_bad_request('No Apply Record ID')
        return make_json_response(HttpResponseBadRequest, resp)

    try:
        anchor_apply_record = AnchorApplyRecord.objects.get(anchor_apply_record_id=anchor_apply_reocrd_id)
    except Exception as e:
        resp = init_http_bad_request('No Match Apply Record')
        return make_json_response(HttpResponseBadRequest, resp)

    if anchor_apply_record.status != AnchorAuditStatus.unaudit.value:
        resp = init_http_bad_request('Anchor Had Been Audited')
        return make_json_response(HttpResponseBadRequest, resp)

    if action == 'pass':
        level = param.get('level', 1)

        anchor_type = AnchorType.objects.get(anchor_type_id=level)
        anchor = anchor_apply_record.audit_pass(auditor, anchor_type)
        send_audit_pass_message(anchor, anchor_apply_record)
    elif action == 'reject':
        anchor_apply_record.audit_fail(auditor)
        send_audit_reject_message(anchor_apply_record)

    results = dict(
        id=anchor_apply_record.anchor_apply_record_id,
        name=anchor_apply_record.nickname,
        status=dict(AnchorAuditStatus.AnchorAuditStatusChoice.value)[anchor_apply_record.status]
    )
    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)
