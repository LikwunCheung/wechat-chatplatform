# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Product, ProductType


class ProductAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'name', 'nickname', 'gender', 'age', 'type_id', 'mobile', 'status')
    list_filter = ('type_id', 'gender', 'status')
    search_fields = ('name', 'nickname',)
    exclude = ('age',)
    empty_value_display = 'N/A'


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('type_id', 'name', 'status',)
    list_filter = ('status',)


class EmployeeGroupAdmin(admin.ModelAdmin):
    list_display = ('group_id', 'dingding_id', 'gender', 'status',)


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeType, EmployeeTypeAdmin)
admin.site.register(EmployeeGroup, EmployeeGroupAdmin)