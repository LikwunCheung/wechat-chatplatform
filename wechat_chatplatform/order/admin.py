# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Order


# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'employee_id', 'product_id', 'status', 'rmb_amount', 'order_time')
    list_filter = ('employee_id', 'status', )
    search_fields = ('employee_id',)
    empty_value_display = 'N/A'
    date_hierarchy = 'order_time'


admin.site.register(Order, OrderAdmin)
