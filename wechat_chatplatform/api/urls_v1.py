# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import path

from wechat_chatplatform.api.views.employees import *
from wechat_chatplatform.api.views.employee_applay import *
from wechat_chatplatform.api.views.information import *


urlpatterns = [
    path('anchor/list/', anchor_list_router),
    path('anchor/detail/', anchor_detail_router),
    path('anchor/apply/', anchor_apply_router),
    path('anchor/apply/gender/', get_gender),g
    path('anchor/apply/city/', get_city),
    path('anchor/apply/level/', get_level),
    path('anchor/apply/unaudit/', anchor_apply_unaudit_router),
    path('anchor/apply/audit/<str:action>/', anchor_apply_action_router),
]
