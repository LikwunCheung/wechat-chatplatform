# -*- coding: utf-8 -*-

import ujson

from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods

from wechat_chatplatform.anchor.models import Anchor, AnchorType, AnchorGroup, AnchorCity
from wechat_chatplatform.common.utils import *
from wechat_chatplatform.common.config import *
from wechat_chatplatform.common.choices import *
from wechat_chatplatform.handler.anchor_handler import anchor_handler


@require_http_methods(['GET', 'OPTIONS'])
@check_api_key
def anchor_list_router(request, *args, **kwargs):
    index = request.GET.get('index', None)

    if index == None:
        return HttpResponseRedirect(DOMAIN + ANCHOR_REDIRECT)
    if request.method == 'GET':
        return anchor_list_get(request, index)
    return HttpResponseNotAllowed()


@require_http_methods(['GET', 'OPTIONS'])
@check_api_key
def anchor_detail_router(requset, *args, **kwargs):
    anchor_id = None
    for arg in args:
        if isinstance(arg, dict):
            index = arg.get('anchor_id', None)

    if anchor_id == None:
        return HttpResponseRedirect(DOMAIN + ANCHOR_REDIRECT)
    if requset.method == 'GET':
        return anchor_detail_get(requset, index)
    return HttpResponseNotAllowed()


def anchor_list_get(request, index):
    mode = request.GET.get('mode', 'default')
    anchors = Anchor.objects.filter(status=AnchorStatus.active.value)
    print(anchors)
    for anchor in anchors:
        print(anchor)

    resp = init_http_success()
    return make_json_response(HttpResponse, resp)


def anchor_detail_get(request, index):
    mode = request.GET.get('mdoe', 'default')
    anchors = Anchor.objects.all()
    print(anchors)
    for anchor in anchors:
        print(anchor)

    resp = init_http_success()
    return make_json_response(HttpResponse, resp)


if __name__ == '__main__':
    anchor_list_get(None, 0)
