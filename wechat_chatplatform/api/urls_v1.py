# -*- coding: utf-8 -*-

from django.urls import path

from .views.anchor.anchor import anchor_list_router, anchor_detail_router
from .views.anchor.apply_anchor import anchor_apply_router, anchor_apply_unaudit_router, anchor_apply_action_router
from .views.information.information import *
from .views.order.order import *


urlpatterns = [
    path('anchor/list/', anchor_list_router),
    path('anchor/detail/', anchor_detail_router),
    path('anchor/apply/', anchor_apply_router),
    path('anchor/apply/gender/', get_gender),
    path('anchor/apply/tag/', get_tag),
    path('anchor/apply/city/', get_city),
    path('anchor/apply/level/', get_level),
    path('anchor/apply/unaudit/', anchor_apply_unaudit_router),
    path('anchor/apply/audit/<str:action>/', anchor_apply_action_router),

    path('order/new/', new_order_router),
]
