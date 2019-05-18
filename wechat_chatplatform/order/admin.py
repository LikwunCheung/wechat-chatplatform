# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Order, OrderHistory


# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'anchor_id', 'product_id', 'status', 'order_type', 'renew_order', 'number', 'rmb_amount', 'order_time')
    list_filter = ('anchor_id', 'status', )
    search_fields = ('anchor_id',)
    empty_value_display = 'N/A'
    date_hierarchy = 'order_time'


class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('order_history_id', 'date', 'update_date', 'order_number', 'order_amount')
    empty_value_display = 'N/A'


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderHistory, OrderHistoryAdmin)
