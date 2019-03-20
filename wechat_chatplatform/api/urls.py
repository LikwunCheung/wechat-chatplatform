# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import path

from .views.employee import *
from .views.order import *

urlpatterns = [
    path('admin/', admin.site.urls),
]
