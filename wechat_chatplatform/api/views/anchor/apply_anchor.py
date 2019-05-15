# -*- coding: utf-8 -*-

import ujson
from datetime import datetime

from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods
from django.utils.timezone import now

from wechat_chatplatform.anchor.models import Anchor, AnchorType, AnchorGroup, AnchorCity, AnchorTag
from wechat_chatplatform.common.utils import *
from wechat_chatplatform.common.config import *
from wechat_chatplatform.common.choices import *
from wechat_chatplatform.handler.anchor_handler import AnchorHandler


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


def anchor_apply_post(request):
    keys = ['name', 'nickname', 'city_id', 'identity_type', 'identity', 'birthday', 'gender', 'mobile', 'wechat_id',
            'audio', 'avatar', 'image', 'slogan', 'tags']

    param = ujson.loads(request.body)
    print(param)

    try:
        for i in range(len(param['image'])):
            param.update({'img{}'.format(i + 1): param['image'][i]})
        param.pop('image')
        param['tags'] = ','.join([str(tag) for tag in param['tags']])
        param['city_id'] = AnchorCity.objects.get(city_id=param['city_id'])
        param['identity_type'] = IdentityType.identity.value
    except Exception as e:
        print(e)
        resp = init_http_bad_request('AttributeError')
        return make_json_response(HttpResponseBadRequest, resp)

    param.update(dict(
        status=AnchorStatus.unaudit.value
    ))

    anchor = anchor_handler.apply_anchor(param)

    resp = init_http_success()
    resp['data'].update(dict(id=anchor.anchor_id))
    return make_json_response(HttpResponse, resp)


def anchor_apply_unaudit_get(request):

    anchors = Anchor.objects.filter(status=AnchorStatus.unaudit.value)
    results = []

    for anchor in anchors:
        img = []
        tags = []
        img.append(anchor.img1) if anchor.img1 else None
        img.append(anchor.img2) if anchor.img2 else None
        img.append(anchor.img3) if anchor.img3 else None
        if anchor.tags:
            _tags = anchor.tags.split(',')
            for tag in _tags:
                try:
                    tag_name = AnchorTag.objects.values('name').get(tag_id=int(tag))
                    tags.append(tag_name['name'])
                except Exception as e:
                    continue

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
                img=img,
                slogan=anchor.slogan,
                tags=tags
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
