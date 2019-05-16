# -*- coding: utf-8 -*-

import ujson

from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page

from wechat_chatplatform.anchor.models import Anchor, AnchorType, AnchorTag
from wechat_chatplatform.common.utils.utils import *
from wechat_chatplatform.common.choices import *


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
    results = [dict(id=level['type_id'], name=level['name']) for level in levels]

    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)


@require_http_methods(['GET'])
@check_api_key
@cache_page(15 * 60)
def get_anchor_city(request, *args, **kwargs):
    levels = Anchor.objects.distinct().values('city').filter(status=Status.active.value)
    results = [item['city'] for item in levels]

    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)


@require_http_methods(['GET'])
@check_api_key
@cache_page(15 * 60)
def get_tag(request, *args, **kwargs):
    tags = AnchorTag.objects.values('name').filter(status=Status.active.value)
    results = [('#' + tag['name']) for tag in tags]

    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)


@require_http_methods(['GET'])
@check_api_key
@cache_page(15 * 60)
def get_product_type(request, *args, **kwargs):
    anchor_id = request.GET.get('id', None)

    if not anchor_id:
        resp = init_http_bad_request('No Anchor ID')
        return make_json_response(HttpResponseBadRequest, resp)

    try:
        anchor = Anchor.objects.get(anchor_id=anchor_id)
    except Exception as e:
        resp = init_http_bad_request('Invalid Anchor ID')
        return make_json_response(HttpResponseBadRequest, resp)

    if anchor.status != AnchorStatus.active.value:
        resp = init_http_bad_request('Invalid Anchor ID')
        return make_json_response(HttpResponseBadRequest, resp)

    products = anchor.type_id.products.filter(status=Status.active.value)
    results = list()
    temp = list()
    for product in products:
        if product.product_id.product_type_id.product_type_id not in temp:
            results.append(dict(id=product.product_id.product_type_id.product_type_id, name=product.product_id.product_type_id.name))
            temp.append(product.product_id.product_type_id.product_type_id)

    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)


@require_http_methods(['GET'])
@check_api_key
@cache_page(15 * 60)
def get_product(request, *args, **kwargs):
    anchor_id = request.GET.get('id', None)
    product_type = request.GET.get('type', None)

    if not anchor_id or not product_type:
        resp = init_http_bad_request('No Anchor ID or No Type')
        return make_json_response(HttpResponseBadRequest, resp)

    try:
        anchor = Anchor.objects.get(anchor_id=anchor_id)
    except Exception as e:
        resp = init_http_bad_request('Invalid Anchor ID')
        return make_json_response(HttpResponseBadRequest, resp)

    if anchor.status != AnchorStatus.active.value:
        resp = init_http_bad_request('Invalid Anchor ID')
        return make_json_response(HttpResponseBadRequest, resp)

    products = anchor.type_id.products.filter(status=Status.active.value)
    results = list()
    for product in products:
        if product.product_id.product_type_id.product_type_id == int(product_type):
            results.append(dict(id=product.product_id.product_id, name=product.product_id.name, price=product.price))

    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)
