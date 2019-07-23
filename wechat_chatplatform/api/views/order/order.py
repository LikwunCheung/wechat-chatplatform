# -*- coding: utf-8 -*-

import ujson
import logging
from datetime import datetime

from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods
from django.utils.timezone import now

from wechat_chatplatform.anchor.models import Anchor, AnchorType
from wechat_chatplatform.user_info.models import UserInfo
from wechat_chatplatform.order.models import Order
from wechat_chatplatform.common.utils.utils import *
from wechat_chatplatform.common.utils.dingtalk_robot_utils import send_new_order_message, send_accept_order_message, \
    send_random_order_message, send_ungrab_order_message
from wechat_chatplatform.common.utils.currency import AUD_CNY
from wechat_chatplatform.common.choices import *
from wechat_chatplatform.common.config import DOMAIN
from wechat_chatplatform.handler.wechat_handler.wechat_handler import wechat_handler

logger = logging.getLogger('django')


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
    if not request.session.get('is_login', False) or not request.session.get('id', None):
        return HttpResponseRedirect(wechat_handler.get_code_url(state='#/order'))

    if request.method == 'GET':
        if request.session.get('is_user', False):
            return user_order_list_get(request)
        if request.session.get('is_anchor', False):
            return anchor_order_list_get(request)
    return HttpResponseNotAllowed()


@require_http_methods(['GET'])
@check_api_key
def order_detail_router(request, *args, **kwargs):
    if not request.session.get('is_login', False) or not request.session.get('id', None):
        return HttpResponseRedirect(wechat_handler.get_code_url(state='#/order'))

    if request.method == 'GET':
        if request.session.get('is_user', False):
            return user_order_detail_get(request)
        if request.session.get('is_anchor', False):
            return anchor_order_detail_get(request)
    return HttpResponseNotAllowed()


@require_http_methods(['GET'])
@check_api_key
def order_detail_receive_router(request, *args, **kwargs):
    if not request.session.get('is_login', False) or not request.session.get('id', None):
        return HttpResponseRedirect(wechat_handler.get_code_url(state='#/order'))

    if request.method == 'GET':
        if request.session.get('is_anchor', False):
            return anchor_order_detail_receive_get(request)
    return HttpResponseNotAllowed()


@require_http_methods(['POST'])
@check_api_key
def order_cancel_router(request, *args, **kwargs):
    if not request.session.get('is_login', False) or not request.session.get('id', None):
        return HttpResponseRedirect(wechat_handler.get_code_url(state='#/order'))

    if request.method == 'POST':
        return order_cancel_post(request)
    return HttpResponseNotAllowed()


@require_http_methods(['GET'])
@check_api_key
def order_salary_router(request, *args, **kwargs):
    if not request.session.get('is_login', False) or not request.session.get('id', None):
        return HttpResponseRedirect(wechat_handler.get_code_url(state='#/order'))

    if request.method == 'GET' and request.session.get('is_anchor', False):
        return anchor_salary_get(request)
    return HttpResponseNotAllowed()


def new_order_post(request):
    keys = ['id', 'product_id', 'number', 'wechat_id', 'comment']
    param = ujson.loads(request.body)
    param = make_dict(keys, param)

    user_id = request.session.get('id', None)
    is_user = request.session.get('is_user', False)
    is_anchor = request.session.get('is_anchor', False)
    if not (user_id and (is_user or is_anchor)):
        return HttpResponseRedirect(wechat_handler.get_code_url(state='#/detail?id={}'.format(param['id'])))

    if is_user:
        user = UserInfo.objects.get(user_id=user_id)
    elif is_anchor:
        anchor = Anchor.objects.get(anchor_id=user_id)
        user = UserInfo.objects.get(open_id=anchor.open_id)

    try:
        anchor = Anchor.objects.get(anchor_id=param['id'], status=AnchorStatus.active.value)
    except Exception as e:
        print(e)
        resp = init_http_bad_request(u'下单失败')
        make_json_response(HttpResponseBadRequest, resp)

    history_orders = Order.objects.filter(status__gte=OrderStatus.salary.value, anchor=anchor, user=user)
    renew_order = OrderRenew.renew.value if history_orders else OrderRenew.first.value

    product_anchor = anchor.anchor_type.products.get(product_anchor_type_id=int(param['product_id']))
    param.pop('id')
    param.pop('product_id')
    param.update(dict(
        # user_id=None,
        user=user,
        product_anchor=product_anchor,
        anchor=anchor,
        anchor_type=anchor.anchor_type,
        order_type=OrderType.normal.value,
        renew=renew_order,
        gender=None,
        # status=OrderStatus.unpaid.value,
        status=OrderStatus.unacknowledge.value,
        origin_amount=round(product_anchor.price * int(param['number']), 2),
        deduction=0,
        total_amount=round(product_anchor.price * int(param['number']), 2),
        rmb_amount=round(product_anchor.price * int(param['number']) * AUD_CNY.get(), 2),
        order_time=now(),
    ))
    order = Order(**param)
    order.save()

    send_new_order_message(order)
    resp = init_http_success()
    resp['data'].update(dict(
        id=order.order_id,
        product=product_anchor.__str__(),
        amount=round(order.rmb_amount, 2)
    ))
    return make_json_response(HttpResponse, resp)


def random_order_post(request):
    keys = ['product_id', 'wechat_id', 'comment', 'tags', 'level', 'gender']
    param = ujson.loads(request.body)
    param = make_dict(keys, param)

    user_id = request.session.get('id', None)
    is_user = request.session.get('is_user', False)
    is_anchor = request.session.get('is_anchor', False)
    if not (user_id and (is_user or is_anchor)):
        logger.warning('No Session ID[%s]: %s%s' % (user_id, request.META['HTTP_HOST'], request.path))
        return HttpResponseRedirect(wechat_handler.get_code_url())

    if is_user:
        user = UserInfo.objects.get(user_id=user_id)
    elif is_anchor:
        anchor = Anchor.objects.get(anchor_id=user_id)
        user = UserInfo.objects.get(open_id=anchor.open_id)

    anchor_type = AnchorType.objects.get(anchor_type_id=param['level'])
    product_anchor = anchor_type.products.get(product_anchor_type_id=int(param['product_id']))
    param.pop('level')
    param.pop('product_id')
    tags = param.pop('tags', u'无')
    if isinstance(tags, list):
        tags = ','.join([tag.strip('#') for tag in tags])

    param.update(dict(
        # user_id=None,
        user=user,
        product_anchor=product_anchor,
        anchor=None,
        order_type=OrderType.random.value,
        renew=OrderRenew.first.value,
        number=1,
        anchor_type=anchor_type,
        gender=param['gender'],
        # status=OrderStatus.unpaid.value,
        status=OrderStatus.ungrab.value,
        origin_amount=round(product_anchor.price, 2),
        deduction=0,
        total_amount=round(product_anchor.price, 2),
        rmb_amount=round(product_anchor.price * AUD_CNY.get(), 2),
        order_time=now(),
    ))
    order = Order(**param)
    order.save()

    send_random_order_message(order, tags=tags)
    resp = init_http_success()
    resp['data'].update(dict(
        id=order.order_id,
        product=product_anchor.__str__(),
        amount=round(order.rmb_amount, 2)
    ))
    return make_json_response(HttpResponse, resp)


def dingtalk_accept_order(request):
    order_id = request.GET.get('id', None)
    anchor_id = request.GET.get('anchor_id', None)
    if not order_id:
        resp = init_http_bad_request('No Order ID')
        return make_json_response(HttpResponseBadRequest, resp)

    try:
        if not anchor_id:
            order = Order.objects.get(order_id=order_id, status=OrderStatus.unacknowledge.value)
        else:
            order = Order.objects.get(order_id=order_id, status=OrderStatus.ungrab.value)
    except Exception as e:
        if anchor_id:
            send_ungrab_order_message(anchor_id)
        resp = init_http_bad_request('No Order ID')
        return make_json_response(HttpResponseBadRequest, resp)

    order.status = OrderStatus.salary.value
    if anchor_id:
        order.anchor = Anchor.objects.get(anchor_id=anchor_id, status=AnchorStatus.active.value,
                                          anchor_type__anchor_type_id__lte=order.anchor_type.anchor_type_id)
    order.complete_time = now()
    order.save()

    request.session['id'] = order.anchor.anchor_id
    request.session['type'] = order.anchor.anchor_type.anchor_type_id
    request.session['is_admin'] = False
    request.session['is_anchor'] = True
    request.session['is_user'] = False
    request.session['is_login'] = True
    request.session.set_expiry(60 * 60)

    send_accept_order_message(order)
    return HttpResponseRedirect(DOMAIN + ORDER_PAGE)


def user_order_list_get(request):
    # user_id = request.session.get('id', None)
    user_id = request.session.get('id', 1)

    if not user_id:
        resp = init_http_bad_request('Error ID')
        return make_json_response(HttpResponseBadRequest, resp)

    try:
        user = UserInfo.objects.get(user_id=user_id)
        orders = user.orders.all().order_by('-order_time')
    except Exception as e:
        resp = init_http_bad_request('Error ID')
        return make_json_response(HttpResponseBadRequest, resp)

    results = list()
    for order in orders:
        results.append(dict(
            id=order.order_id,
            anchor=order.anchor.nickname if order.anchor else None,
            avatar=order.anchor.avatar if order.anchor else None,
            product=order.product_anchor.__str__(),
            number=order.number,
            status=dict(OrderStatus.OrderStatusChoices.value)[
                (OrderStatus.close.value if order.status >= OrderStatus.salary.value else order.status)],
            amount=round(order.rmb_amount, 2),
            time=order.order_time,
            detail=True if order.status > 0 else False,
        ))
    resp = init_http_success()
    resp.update(
        type=0,
        data=results
    )
    return make_json_response(HttpResponse, resp)


def anchor_order_list_get(request):
    # anchor_id = request.session.get('id', None)
    anchor_id = request.session.get('id', 2)

    if not anchor_id:
        resp = init_http_bad_request('Error ID')
        return make_json_response(HttpResponseBadRequest, resp)

    try:
        anchor = Anchor.objects.get(status=AnchorStatus.active.value, anchor_id=anchor_id)
        orders = anchor.orders.all().order_by('-order_time')
    except Exception as e:
        resp = init_http_bad_request('Error ID')
        return make_json_response(HttpResponseBadRequest, resp)

    my_orders = None
    try:
        user = UserInfo.objects.get(open_id=anchor.open_id)
        my_orders = user.orders.all().order_by('-order_time')
    except Exception as e:
        pass

    results = list()
    my_results = list()
    for order in orders:
        partition = order.product_anchor.product.partition if order.renew == OrderRenew.first.value else order.product_anchor.product.partition_extend
        results.append(dict(
            id=order.order_id,
            renew=dict(OrderRenew.OrderRenewChoices.value)[order.renew],
            type=dict(OrderType.OrderTypeChoices.value)[order.order_type],
            product=order.product_anchor.__str__(),
            number=order.number,
            status=dict(OrderStatus.OrderStatusChoices.value)[order.status],
            amount=round(order.rmb_amount * partition, 2),
            time=order.order_time,
            detail=True if order.status > 0 else False,
        ))

    if my_orders:
        for order in my_orders:
            my_results.append(dict(
                id=order.order_id,
                anchor=order.anchor.nickname if order.anchor else None,
                avatar=order.anchor.avatar if order.anchor else None,
                product=order.product_anchor.__str__(),
                number=order.number,
                status=dict(OrderStatus.OrderStatusChoices.value)[
                    (OrderStatus.close.value if order.status >= OrderStatus.salary.value else order.status)],
                amount=round(order.rmb_amount, 2),
                time=order.order_time,
                detail=True if order.status > 0 else False,
            ))

    resp = init_http_success()
    resp.update(
        type=1,
        data=my_results,
        data1=results
    )
    return make_json_response(HttpResponse, resp)


def user_order_detail_get(request):
    order_id = request.GET.get('id', None)
    user_id = request.session.get('id', 1)
    is_user = request.session.get('is_user', False)

    if not order_id or not user_id:
        resp = init_http_bad_request('Error ID')
        return make_json_response(HttpResponseBadRequest, resp)

    try:
        user = UserInfo.objects.get(user_id=user_id)
        order = Order.objects.get(order_id=order_id, user=user, status__gte=OrderStatus.unpaid.value)
    except Exception as e:
        resp = init_http_bad_request('Error ID')
        return make_json_response(HttpResponseBadRequest, resp)

    results = dict(
        id=order.order_id,
        anchor=order.anchor.nickname if order.anchor else None,
        product_type=order.product_anchor.product.product_type.name,
        product=order.product_anchor.product.name,
        price=order.product_anchor.price,
        number=order.number,
        amount=round(order.total_amount, 2),
        rmb_amount=round(order.rmb_amount, 2),
        order_time=order.order_time,
        wechat_id=order.wechat_id,
        comment=order.comment,
        status=dict(OrderStatus.OrderStatusChoices.value)[
            (OrderStatus.close.value if order.status >= OrderStatus.salary.value else order.status)],
        modify=True if order.status == OrderStatus.unpaid.value else False,
    )

    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)


def anchor_order_detail_get(request):
    order_id = request.GET.get('id', None)
    anchor_id = request.session.get('id', 2)

    if not order_id or not anchor_id:
        resp = init_http_bad_request('Error ID')
        return make_json_response(HttpResponseBadRequest, resp)

    try:
        anchor = Anchor.objects.get(anchor_id=anchor_id, status=AnchorStatus.active.value)
        user = UserInfo.objects.get(open_id=anchor.open_id)
        order = Order.objects.get(order_id=order_id, user=user, status__gte=OrderStatus.unpaid.value)
        results = dict(
            id=order.order_id,
            anchor=order.anchor.nickname if order.anchor else None,
            product_type=order.product_anchor.product.product_type.name,
            product=order.product_anchor.product.name,
            price=order.product_anchor.price,
            number=order.number,
            amount=round(order.total_amount, 2),
            rmb_amount=round(order.rmb_amount, 2),
            order_time=order.order_time,
            wechat_id=order.wechat_id,
            comment=order.comment,
            status=dict(OrderStatus.OrderStatusChoices.value)[
                (OrderStatus.close.value if order.status >= OrderStatus.salary.value else order.status)],
            modify=True if order.status == OrderStatus.unpaid.value else False
        )
    except Exception as e:
        resp = init_http_bad_request('Error ID')
        return make_json_response(HttpResponseBadRequest, resp)

    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)


def anchor_order_detail_receive_get(request):
    order_id = request.GET.get('id', None)
    anchor_id = request.session.get('id', 2)

    if not order_id or not anchor_id:
        resp = init_http_bad_request('Error ID')
        return make_json_response(HttpResponseBadRequest, resp)

    try:
        anchor = Anchor.objects.get(anchor_id=anchor_id, status=AnchorStatus.active.value)
        order = anchor.orders.get(order_id=order_id, status__gte=OrderStatus.unpaid.value)
        partition = order.product_anchor.product.partition if order.renew == OrderRenew.first.value else order.product_anchor.product.partition_extend
        results = dict(
            id=order.order_id,
            product_type=order.product_anchor.product.product_type.name,
            product=order.product_anchor.product.name,
            price=round(order.product_anchor.price, 2),
            number=order.number,
            amount=round(order.total_amount, 2),
            renew=dict(OrderRenew.OrderRenewChoices.value)[order.renew],
            type=dict(OrderType.OrderTypeChoices.value)[order.order_type],
            rmb_amount=round(order.rmb_amount, 2),
            my_amount=round(order.rmb_amount * partition, 2),
            order_time=order.order_time,
            salary_time=order.salary_time if order.salary_time else None,
            wechat_id=order.wechat_id if order.status >= OrderStatus.salary.value else '******',
            comment=order.comment,
            status=dict(OrderStatus.OrderStatusChoices.value)[order.status],
            modify=False
        )
    except Exception as e:
        resp = init_http_bad_request('Error ID')
        return make_json_response(HttpResponseBadRequest, resp)

    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)


def order_cancel_post(request):
    try:
        param = ujson.loads(request.body)
        order_id = param.get('id', None)
        user_id = request.session.get('id', 1)
        anchor_id = request.session.get('id', 2)
        is_user = request.session.get('is_user', False)
        is_anchor = request.session.get('is_anchor', False)
    except Exception:
        resp = init_http_bad_request('Error ID')
        return make_json_response(HttpResponseBadRequest, resp)

    if not order_id:
        resp = init_http_bad_request('Error ID')
        return make_json_response(HttpResponseBadRequest, resp)

    if is_user:
        try:
            user = UserInfo.objects.get(user_id=user_id)
            order = user.orders.get(order_id=order_id, status=OrderStatus.unpaid.value)
            order.status = OrderStatus.delete.value
            order.save()
        except Exception:
            resp = init_http_bad_request('Error ID')
            return make_json_response(HttpResponseBadRequest, resp)
    elif is_anchor:
        try:
            anchor = Anchor.objects.get(anchor_id=anchor_id, status=AnchorStatus.active.value)
            user = UserInfo.objects.get(open_id=anchor.open_id)
            order = user.orders.get(order_id=order_id, status=OrderStatus.unpaid.value)
            order.status = OrderStatus.delete.value
            order.save()
        except Exception:
            resp = init_http_bad_request('Error ID')
            return make_json_response(HttpResponseBadRequest, resp)
    else:
        return make_json_response(HttpResponseBadRequest, None)

    resp = init_http_success()
    return make_json_response(HttpResponse, resp)


def anchor_salary_get(request):
    anchor_id = request.session.get('id', None)

    if not anchor_id:
        resp = init_http_bad_request('Error ID')
        return make_json_response(HttpResponseBadRequest, resp)

    try:
        anchor = Anchor.objects.get(anchor_id=anchor_id, status=AnchorStatus.active.value)
    except Exception as e:
        resp = init_http_bad_request('Error ID')
        return make_json_response(HttpResponseBadRequest, resp)

    orders = Order.objects.filter(anchor_id=anchor, status=OrderStatus.salary)
    results = dict(
        numbers=len(orders),
        amount=0
    )
    for order in orders:
        results['amount'] += round(order.rmb_amount * (
            order.product_anchor.product.partition if order.renew == OrderRenew.first else order.product_anchor.product.partition_extend), 2)

    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)
