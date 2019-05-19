# -*- coding: utf-8 -*-

import ujson

from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods

from wechat_chatplatform.anchor.models import Anchor
from wechat_chatplatform.common.utils.utils import *
from wechat_chatplatform.common.config import *
from wechat_chatplatform.common.choices import *


@require_http_methods(['GET', 'OPTIONS'])
@check_api_key
def anchor_list_router(request, *args, **kwargs):
    index = request.GET.get('index', None)

    if index == None:
        return HttpResponseRedirect(DOMAIN)
    if request.method == 'GET':
        return anchor_list_get(request, index)
    return HttpResponseNotAllowed()


@require_http_methods(['GET', 'OPTIONS'])
@check_api_key
def anchor_detail_router(requset, *args, **kwargs):
    anchor_id = requset.GET.get('id', None)

    if anchor_id == None:
        return HttpResponseRedirect(DOMAIN)
    if requset.method == 'GET':
        return anchor_detail_get(requset, anchor_id)
    return HttpResponseNotAllowed()


def anchor_list_get(request, index):
    gender = request.GET.get('gender', None)
    level = request.GET.get('level', None)
    city = request.GET.get('city', None)

    index = int(index)

    query_param = dict(
        status=AnchorStatus.active.value,
    )
    if gender:
        query_param.update(dict(gender=gender))
    if level:
        query_param.update(dict(anchor_type=level))
    if city:
        query_param.update(dict(city=city))

    try:
        anchors = Anchor.objects.filter(**query_param).order_by('anchor_type')[index * 8: (index + 1) * 8]
    except Exception as e:
        print(e)
        resp = init_http_bad_request('No Match Record')
        return make_json_response(HttpResponseBadRequest, resp)

    results = list()
    for anchor in anchors:
        anchor_products = anchor.anchor_type.products.all().order_by('price')

        results.append(dict(
            id=anchor.anchor_id,
            nickname=anchor.nickname,
            gender=anchor.gender,
            constellation=anchor.constellation(),
            slogan=anchor.slogan,
            age=anchor.age(),
            level=anchor.anchor_type.name,
            audio=anchor.audio,
            avatar=anchor.avatar,
            price=anchor_products[0].price if anchor_products else 15,
        ))

    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)


def anchor_detail_get(request, anchor_id):
    anchor_id = int(anchor_id)

    anchor = Anchor.objects.get(anchor_id=anchor_id)
    if anchor.status != AnchorStatus.active.value:
        resp = init_http_bad_request('Wrong Anchor ID')
        return make_json_response(HttpResponseBadRequest, resp)

    anchor_products = anchor.anchor_type.products.values('product__product_type__name', 'product__name',
                                                         'product__time', 'price').filter(
        status=Status.active.value).order_by('product__time')

    anchor_product_types = list(
        set([anchor_product['product__product_type__name'] for anchor_product in anchor_products]))

    anchor_product_times = list()
    for anchor_product in anchor_products:
        if anchor_product['product__name'] not in anchor_product_times:
            anchor_product_times.append(anchor_product['product__name'])
    anchor_product_times = [[item] + [''] * len(anchor_product_types) for item in anchor_product_times]

    for anchor_product in anchor_products:
        for anchor_product_time in anchor_product_times:
            if anchor_product_time[0] == anchor_product['product__name']:
                index = anchor_product_types.index(anchor_product['product__product_type__name']) + 1
                anchor_product_time[index] = anchor_product['price']

    results = dict(
        id=anchor.anchor_id,
        nickname=anchor.nickname,
        gender=anchor.gender,
        constellation=anchor.constellation(),
        slogan=anchor.slogan,
        age=anchor.age(),
        level=anchor.anchor_type.name,
        audio=anchor.audio,
        image=anchor.image.split(',') if anchor.image else None,
        avatar=anchor.avatar,
        product_type=anchor_product_types,
        product=anchor_product_times,
        tags=['#' + tag for tag in anchor.tags.split(',')] if anchor.tags else None
    )

    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)


if __name__ == '__main__':
    anchor_list_get(None, 0)
