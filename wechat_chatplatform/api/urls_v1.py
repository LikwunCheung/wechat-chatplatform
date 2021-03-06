# -*- coding: utf-8 -*-

from django.urls import path, include

from .views.anchor.anchor import anchor_list_router, anchor_detail_router
from .views.anchor.apply_anchor import anchor_apply_router, anchor_apply_unaudit_router, anchor_apply_action_router
from .views.information.information import *
from .views.order.order import *
from .views.oauth import *
from .views.admin_user import *

urlpatterns = [
    path('anchor/list/', anchor_list_router),
    path('anchor/detail/', anchor_detail_router),

    path('anchor/apply/', anchor_apply_router),
    path('anchor/apply/unaudit/', anchor_apply_unaudit_router),
    path('anchor/apply/audit/<str:action>/', anchor_apply_action_router),

    path('info/gender/', get_gender),
    path('info/tag/', get_tag),
    path('info/city/', get_anchor_city),
    path('info/aud-rate/', get_aud_rate),
    path('info/level/', get_anchor_level),
    path('info/product-type/', get_product_type),
    path('info/product/', get_product),
    path('info/platform/', platform_info_router),

    # path('anchor/apply/audit/dingtalk/<str:action>/', anchor_apply_dingtalk_action_router),

    path('order/new/', new_order_router),
    path('order/random/', random_order_router),
    path('order/accept/', dingtalk_accept_order),
    path('order/list/', order_list_router),
    path('order/detail/', order_detail_router),
    path('order/detail/receive/', order_detail_receive_router),
    path('order/cancel/', order_cancel_router),
    path('order/salary/', order_salary_router),
    path('order/random/accept/', dingtalk_accept_order),

    path('wxoauth/recall/', oauth_router),

    path('admin/login/', admin_user_login),
    path('admin/user/info/', get_user_info),
    path('admin/user/logout/', admin_user_logout),
    path('admin/user/update/', admin_user_update),
    path('admin/user/remove/', admin_user_remove),
    path('admin/user/', admin_user_router),
    path('admin/type/', get_admin_type),
]
