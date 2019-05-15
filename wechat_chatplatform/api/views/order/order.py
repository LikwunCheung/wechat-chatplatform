# -*- coding: utf-8 -*-

import ujson
from datetime import datetime

from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods
from django.utils.timezone import now

from wechat_chatplatform.anchor.models import Anchor, AnchorType, AnchorGroup, AnchorTag
from wechat_chatplatform.common.utils.utils import *
from wechat_chatplatform.common.config import *
from wechat_chatplatform.common.choices import *


@require_http_methods(['POST', 'OPTIONS'])
@check_api_key
def new_order_router(request, *args, **kwargs):

    if request.method == 'POST':
        return new_order_post(request)
    return HttpResponseNotAllowed()


def new_order_post(request):
    keys = ['']
    param = ujson.loads(request.body)


