# -*- coding: utf-8 -*-

import ujson
from datetime import datetime

from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods
from django.utils.timezone import now

from wechat_chatplatform.anchor.models import Anchor, AnchorType
from wechat_chatplatform.user_info.models import UserInfo
from wechat_chatplatform.order.models import Order
from wechat_chatplatform.common.utils.utils import *
from wechat_chatplatform.common.utils.dingtalk_robot_utils import send_new_order_message, send_accept_order_message, \
    send_random_order_message
from wechat_chatplatform.common.utils.currency import AUD_CNY
from wechat_chatplatform.common.choices import *
from wechat_chatplatform.common.config import DOMAIN
from wechat_chatplatform.handler.wechat_handler.wechat_handler import wechat_handler


@require_http_methods(['POST', 'OPTIONS'])
@check_api_key
def new_order_router(request, *args, **kwargs):
    if request.method == 'POST':
        return new_order_post(request)
    return HttpResponseNotAllowed()


@require_http_methods(['POST', 'OPTIONS'])
@check_api_key
def random_order_router(request, *args, **kwargs):
    if request.method == 'POST':
        return random_order_post(request)
    return HttpResponseNotAllowed()


@require_http_methods(['GET'])
@check_api_key
def order_list_router(request, *args, **kwargs):
    # if not request.session.get('is_login', False) or not request.session.get('id', None):
    #     return HttpResponseRedirect(wechat_handler.get_code_url(state='#/order'))

    if request.method == 'GET':
        # if request.session.get('is_user', False):
        #     return user_order_list_get(request)
        # if request.session.get('is_anchor', False):
        return anchor_order_list_get(request)
    return HttpResponseNotAllowed()


def new_order_post(request):
    keys = ['id', 'product_id', 'number', 'wechat_id', 'comment']
    param = ujson.loads(request.body)
    param = make_dict(keys, param)

    user_id = request.session.get('id', None)
    is_user = request.session.get('is_user', False)
    if not (user_id and is_user):
        return HttpResponseRedirect(wechat_handler.get_code_url(state='#/detail?id={}'.format(param['id'])))
    user = UserInfo.objects.get(user_id=user_id)

    try:
        anchor = Anchor.objects.get(anchor_id=param['id'], status=AnchorStatus.active.value)
    except Exception as e:
        print(e)
        resp = init_http_bad_request(u'下单失败')
        make_json_response(HttpResponseBadRequest, resp)

    history_orders = Order.objects.filter(status__gte=OrderStatus.salary.value, anchor_id=anchor, user_id=user_id)
    renew_order = OrderRenew.renew.value if history_orders else OrderRenew.first.value

    product = anchor.type_id.products.get(product_id=int(param['product_id']))
    param.pop('id')
    param.update(dict(
        # user_id=None,
        user_id=user,
        product_id=product,
        anchor_id=anchor,
        anchor_type_id=None,
        order_type=OrderType.normal.value,
        renew_order=renew_order,
        gender=None,
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


def random_order_post(request):
    keys = ['product_id', 'number', 'wechat_id', 'comment', 'tags', 'level', 'gender']
    param = ujson.loads(request.body)
    param = make_dict(keys, param)

    user_id = request.session.get('id', None)
    is_user = request.session.get('is_user', False)
    if not (user_id and is_user):
        return HttpResponseRedirect(wechat_handler.get_code_url())
    user = UserInfo.objects.get(user_id=user_id)

    anchor_type = AnchorType.objects.get(type_id=param['level'])
    product = anchor_type.products.get(product_id=int(param['product_id']))
    param.pop('level')
    tags = param.pop('tags', u'无')
    param.update(dict(
        # user_id=None,
        user_id=user,
        product_id=product,
        anchor_id=None,
        order_type=OrderType.random.value,
        renew_order=OrderRenew.first.value,
        anchor_type_id=anchor_type,
        gender=param['gender'],
        status=OrderStatus.unpaid.value,
        origin_amount=product.price * param['number'],
        deduction=0,
        total_amount=product.price * param['number'],
        rmb_amount=round(product.price * param['number'] * AUD_CNY.get(), 2),
        order_time=now(),
    ))
    order = Order(**param)
    order.save()

    send_random_order_message(order, tags=tags)
    resp = init_http_success()
    resp['data'].update(dict(
        id=order.order_id,
        product=product.__str__(),
        amount=order.rmb_amount
    ))
    return make_json_response(HttpResponse, resp)


def dingtalk_accept_order(request):
    order_id = request.GET.get('id', None)
    if not order_id:
        resp = init_http_bad_request('No Order ID')
        return make_json_response(HttpResponseBadRequest, resp)

    try:
        order = Order.objects.get(order_id=order_id, status=OrderStatus.unacknowledge.value)
    except Exception as e:
        resp = init_http_bad_request('No Order ID')
        return make_json_response(HttpResponseBadRequest, resp)

    order.status = OrderStatus.salary.value
    order.complete_time = now()
    order.save()

    send_accept_order_message(order)
    return HttpResponseRedirect(DOMAIN)


def user_order_list_get(request):
    # user_id = request.session.get('id', None)
    user_id = request.session.get('id', 2)

    if not user_id:
        resp = init_http_bad_request('Error ID')
        return make_json_response(HttpResponseBadRequest, resp)

    try:
        user = UserInfo.objects.get(user_id=user_id)
        orders = user.user.all().order_by('order_time')
    except Exception as e:
        resp = init_http_bad_request('Error ID')
        return make_json_response(HttpResponseBadRequest, resp)

    results = list()
    for order in orders:
        results.append(dict(
            id=order.order_id,
            anchor=order.anchor_id.nickname,
            avatar=order.anchor_id.avatar,
            product=order.product_id.__str__(),
            number=order.number,
            status=dict(OrderStatus.OrderStatusChoices.value)[order.status],
            amount=order.rmb_amount,
            time=order.order_time.strftime('%Y-%m-%d %H:%m:%S')
        ))
    resp = init_http_success()
    resp.update(
        type=0,
        data=results
    )
    return make_json_response(HttpResponse, resp)


def anchor_order_list_get(request):
    # anchor_id = request.session.get('id', None)
    anchor_id = request.session.get('id', 5)

    if not anchor_id:
        resp = init_http_bad_request('Error ID')
        return make_json_response(HttpResponseBadRequest, resp)

    try:
        anchor = Anchor.objects.get(status=AnchorStatus.active.value, anchor_id=anchor_id)
        orders = anchor.order.all().order_by('order_time')
    except Exception as e:
        resp = init_http_bad_request('Error ID')
        return make_json_response(HttpResponseBadRequest, resp)

    results = list()
    for order in orders:
        results.append(dict(
            id=order.order_id,
            anchor=anchor.nickname,
            product=order.product_id.__str__(),
            number=order.number,
            status=dict(OrderStatus.OrderStatusChoices.value)[order.status],
            amount=order.rmb_amount * (order.product_id.product_id.partition if order.renew_order == OrderRenew.first.value else order.product_id.product_id.partition_extend),
            time=order.order_time.strftime('%Y-%m-%d %H:%m:%S')
        ))
    resp = init_http_success()
    resp.update(
        type=1,
        data=results
    )
    return make_json_response(HttpResponse, resp)
