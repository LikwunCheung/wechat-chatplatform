# -*- coding: utf-8 -*-

from django.urls import path, include

from .views.anchor.anchor import anchor_list_router, anchor_detail_router
from .views.anchor.apply_anchor import anchor_apply_router, anchor_apply_unaudit_router, anchor_apply_action_router
from .views.information.information import *
from .views.order.order import *

urlpatterns = [
    path('anchor/list/', anchor_list_router),
    path('anchor/detail/', anchor_detail_router),

    path('anchor/apply/', anchor_apply_router),
    path('anchor/apply/unaudit/', anchor_apply_unaudit_router),
    path('anchor/apply/audit/<str:action>/', anchor_apply_action_router),

    path('info/gender/', get_gender),
    path('info/tag/', get_tag),
    path('info/city/', get_anchor_city),
    path('info/level/', get_anchor_level),
    path('info/product-type/', get_product_type),
    path('info/product/', get_product),

    # path('anchor/apply/audit/dingtalk/<str:action>/', anchor_apply_dingtalk_action_router),

    path('order/new/', new_order_router),
]
