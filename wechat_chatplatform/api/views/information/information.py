# -*- coding: utf-8 -*-

import ujson

from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page

from wechat_chatplatform.anchor.models import Anchor, AnchorType, AnchorTag
from wechat_chatplatform.platform_admin.models import AdminUserType
from wechat_chatplatform.platform_info.models import PlatformInfo
from wechat_chatplatform.common.utils.utils import *
from wechat_chatplatform.common.utils.currency import AUD_CNY
from wechat_chatplatform.common.choices import *


@require_http_methods(['GET'])
@check_api_key
@cache_page(15 * 60)
def get_admin_type(request, *args, **kwargs):
    admin_user_types = AdminUserType.objects.filter(status=Status.active.value)

    results = [dict(
        id=admin_user_type.admin_user_type_id,
        name=admin_user_type.name
    ) for admin_user_type in admin_user_types]

    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)


@require_http_methods(['GET'])
@check_api_key
@cache_page(15 * 60)
def get_gender(request, *args, **kwargs):
    results = [dict(id=k, gender=v) for k, v in Gender.GenderChoices.value]

    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)


@require_http_methods(['GET'])
@check_api_key
@cache_page(15 * 60)
def get_aud_rate(request, *args, **kwargs):
    results = dict(rate=AUD_CNY.get())

    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)


@require_http_methods(['GET'])
@check_api_key
@cache_page(15 * 60)
def get_anchor_level(request, *args, **kwargs):
    levels = AnchorType.objects.values('anchor_type_id', 'name').filter(status=Status.active.value)
    results = [dict(
        id=level['anchor_type_id'],
        name=level['name']
    ) for level in levels]

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
    anchor_type_id = request.GET.get('level', None)

    if not anchor_id and not anchor_type_id:
        resp = init_http_bad_request(u'无店员ID/店员等级/产品类型')
        return make_json_response(HttpResponseBadRequest, resp)

    if anchor_id:
        try:
            anchor = Anchor.objects.get(anchor_id=anchor_id, status=AnchorStatus.active.value)
            anchor_type = anchor.anchor_type
        except Exception:
            resp = init_http_bad_request(u'无效店员ID')
            return make_json_response(HttpResponseBadRequest, resp)

    if anchor_type_id:
        try:
            anchor_type = AnchorType.objects.get(anchor_type_id=anchor_type_id, status=Status.active.value)
        except Exception:
            resp = init_http_bad_request(u'无效店员等级')
            return make_json_response(HttpResponseBadRequest, resp)

    products = anchor_type.products.distinct().values(
        'product__product_type__product_type_id', 'product__product_type__name').filter(status=Status.active.value)

    results = [dict(
        id=product['product__product_type__product_type_id'],
        name=product['product__product_type__name']
    ) for product in products]

    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)


@require_http_methods(['GET'])
@check_api_key
@cache_page(15 * 60)
def get_product(request, *args, **kwargs):
    anchor_id = request.GET.get('id', None)
    anchor_type_id = request.GET.get('level', None)
    product_type = request.GET.get('type', None)

    if (not anchor_id and not anchor_type_id) or not product_type:
        resp = init_http_bad_request(u'无店员ID/店员等级/产品类型')
        return make_json_response(HttpResponseBadRequest, resp)

    if anchor_id:
        try:
            anchor = Anchor.objects.get(anchor_id=anchor_id, status=AnchorStatus.active.value)
            anchor_type = anchor.anchor_type
        except Exception:
            resp = init_http_bad_request(u'无效店员ID')
            return make_json_response(HttpResponseBadRequest, resp)

    if anchor_type_id:
        try:
            anchor_type = AnchorType.objects.get(anchor_type_id=anchor_type_id, status=Status.active.value)
        except Exception:
            resp = init_http_bad_request(u'无效店员等级')
            return make_json_response(HttpResponseBadRequest, resp)

    products = anchor_type.products.values('product_anchor_type_id', 'product__name', 'price').filter(
        status=Status.active.value, product__product_type__product_type_id=product_type)

    results = [dict(
        id=product['product_anchor_type_id'],
        name=product['product__name'],
        price=product['price']
    ) for product in products]

    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)


@require_http_methods(['GET', 'POST'])
@check_api_key
def platform_info_router(request, *args, **kwargs):
    if request.method == 'GET':
        return get_platform_info(request, args, kwargs)
    elif request.method == 'POST':
        return post_platform_info(request, args, kwargs)
    else:
        return HttpResponseBadRequest()


@cache_page(15 * 60)
def get_platform_info(request, *args, **kwargs):
    tag = request.GET.get('tag', None)

    if not tag:
        resp = init_http_bad_request(u'无标签参数')
        return make_json_response(HttpResponseBadRequest, resp)

    try:
        platform_info = PlatformInfo.objects.values('content').get(tag=tag, status=Status.active.value)
    except Exception as e:
        resp = init_http_bad_request(u'无匹配标签')
        return make_json_response(HttpResponseBadRequest, resp)

    results = [result.strip('\r\n') for result in platform_info['content'].split(';')]

    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)


def post_platform_info(request, *args, **kwargs):
    param = ujson.loads(request.body)
    tag = param.get('tag', None)
    tag_cn = param.get('tag_cn', None)
    data = param.get('data', None)

    if not (tag and data):
        resp = init_http_bad_request(u'无标签')
        return make_json_response(HttpResponseBadRequest, resp)

    if not isinstance(data, list):
        data = [data]

    content = ';'.join(data)
    platform_info = PlatformInfo.objects.get(tag=tag)
    if platform_info and platform_info.status != Status.active.value:
        resp = init_http_bad_request(u'已停用')
        return make_json_response(HttpResponseBadRequest, resp)
    elif not platform_info:
        platform_info = PlatformInfo(tag=tag, tag_cn=tag_cn, content=content, status=Status.active.value)
        platform_info.save()
    else:
        platform_info.content = content
        platform_info.save()

    resp = init_http_success()
    return make_json_response(HttpResponse, resp)



