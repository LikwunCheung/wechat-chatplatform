# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('v1/', include('wechat_chatplatform.api.urls_v1')),
]
