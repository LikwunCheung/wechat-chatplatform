# -*- coding: utf-8 -*-

import ujson

from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page

from wechat_chatplatform.anchor.models import Anchor, AnchorType, AnchorTag, AnchorCity
from wechat_chatplatform.common.utils.utils import *
from wechat_chatplatform.common.choices import *


@require_http_methods(['GET'])
@check_api_key
@cache_page(15 * 60)
def get_city(request, *args, **kwargs):
    citys = AnchorCity.objects.values('city_id', 'name').filter(status=Status.active.value)
    print(citys)

    results = []
    for city in citys:
        results.append(dict(
            id=city['city_id'],
            name=city['name']
        ))
    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)


@require_http_methods(['GET'])
@check_api_key
@cache_page(15 * 60)
def get_gender(request, *args, **kwargs):
    results = [dict(id=k, gender=v) for k, v in Gender.GenderChoices.value[0: -1]]

    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)


@require_http_methods(['GET'])
@check_api_key
@cache_page(15 * 60)
def get_anchor_level(request, *args, **kwargs):
    levels = AnchorType.objects.values('type_id', 'name').filter(status=Status.active.value)
    results = []
    for level in levels:
        results.append(dict(
            id=level['type_id'],
            name=level['name']
        ))
    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)


@require_http_methods(['GET'])
@check_api_key
@cache_page(15 * 60)
def get_tag(request, *args, **kwargs):
    tags = AnchorTag.objects.values('name').filter(status=Status.active.value)
    results = []
    for tag in tags:
        results.append(tag['name'])

    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)
