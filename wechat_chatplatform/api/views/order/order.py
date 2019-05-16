# -*- coding: utf-8 -*-

import ujson
from datetime import datetime

from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods
from django.utils.timezone import now

from wechat_chatplatform.anchor.models import Anchor
from wechat_chatplatform.order.models import Order
from wechat_chatplatform.common.utils.utils import *
from wechat_chatplatform.common.utils.dingtalk_robot_utils import send_new_order_message
from wechat_chatplatform.common.utils.currency import AUD_CNY
from wechat_chatplatform.common.choices import *


@require_http_methods(['POST', 'OPTIONS'])
@check_api_key
def new_order_router(request, *args, **kwargs):

    if request.method == 'POST':
        return new_order_post(request)
    return HttpResponseNotAllowed()


@require_http_methods(['GET'])
@check_api_key
def order_list_router(request, *args, **kwargs):
    if request.method == 'GET':
        return order_list_get(request)
    return HttpResponseNotAllowed()


def new_order_post(request):
    keys = ['id', 'product_id', 'number', 'wechat_id', 'comment']
    param = ujson.loads(request.body)
    param = make_dict(keys, param)

    try:
        anchor = Anchor.objects.get(anchor_id=param['id'], status=AnchorStatus.active.value)
    except Exception as e:
        print(e)
        resp = init_http_bad_request(u'下单失败')
        make_json_response(HttpResponseBadRequest, resp)

    product = anchor.type_id.products.get(product_id=int(param['product_id']))
    param.pop('id')
    param.update(dict(
        user_id=None,
        product_id=product,
        anchor_id=anchor,
        gender=anchor.gender,
        status=OrderStatus.unpaid.value,
        origin_amount=product.price * param['number'],
        deduction=0,
        total_amount=product.price * param['number'],
        rmb_amount=round(product.price * param['number'] * AUD_CNY.get(), 2),
        order_time=now(),
    ))
    order = Order(**param)
    order.save()


    resp = init_http_success()
    resp['data'].update(dict(
        id=order.order_id,
        product=product.__str__(),
        amount=order.rmb_amount
    ))
    return make_json_response(HttpResponse, resp)


def random_order_post(request):
    keys = ['product_id', 'number', 'wechat_id', 'comment', 'tags', 'level']
    param = ujson.loads(request.body)
    param = make_dict(keys, param)

    try:
        anchor = Anchor.objects.get(anchor_id=param['id'], status=AnchorStatus.active.value)
    except Exception as e:
        print(e)
        resp = init_http_bad_request(u'下单失败')
        make_json_response(HttpResponseBadRequest, resp)

    product = anchor.type_id.products.get(product_id=int(param['product_id']))
    param.pop('id')
    param.update(dict(
        user_id=None,
        product_id=product,
        anchor_id=anchor,
        gender=anchor.gender,
        status=OrderStatus.unpaid.value,
        origin_amount=product.price * param['number'],
        deduction=0,
        total_amount=product.price * param['number'],
        rmb_amount=round(product.price * param['number'] * AUD_CNY.get(), 2),
        order_time=now(),
    ))
    order = Order(**param)
    order.save()

    send_new_order_message(order)
    resp = init_http_success()
    resp['data'].update(dict(
        id=order.order_id,
        product=product.__str__(),
        amount=order.rmb_amount
    ))
    return make_json_response(HttpResponse, resp)


def order_list_get(request):
    pass


