# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import path

from wechat_chatplatform.api.views.employees import *
from wechat_chatplatform.api.views.employee_applay import *


urlpatterns = [
    path('anchor/list/', anchor_list_router),
    path('anchor/detail/', anchor_detail_router),
    path('anchor/gender/', get_gender),
    path('anchor/apply/unaudit/', anchor_apply_unaudit_router),
    path('anchor/apply/audit/pass/', anchor_apply_pass_router),
    path('anchor/apply/audit/reject/', anchor_apply_reject_router),
]
