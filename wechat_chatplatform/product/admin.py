# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Product, ProductType, ProductEmployeeType


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'type_id', 'name', 'time', 'partition', 'partition_extend', 'status',)
    list_filter = ('type_id', 'status',)
    # search_fields = ('name', 'nickname',)
    empty_value_display = 'N/A'


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('type_id', 'name', 'status',)
    list_filter = ('status',)


class ProductEmployeeTypeAdmin(admin.ModelAdmin):
    list_display = ('product_employee_type_id', 'product_id', 'employee_type_id', 'price', 'status',)
    list_filter = ('product_id', 'employee_type_id', 'status',)


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(ProductEmployeeType, ProductEmployeeTypeAdmin)
