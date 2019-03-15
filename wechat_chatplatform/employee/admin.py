# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Employee, EmployeeType, EmployeeGroup

# Register your models here.
admin.site.site_header = u'后台管理系统'
admin.site.site_title = u'后台管理系统'


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'name', 'nickname', 'gender', 'age', 'type_id', 'mobile', 'status')
    list_filter = ('type_id', 'gender', 'status')
    search_fields = ('name', 'nickname',)
    exclude = ('age',)
    empty_value_display = 'N/A'
    # readonly_fields = ('age',)

class EmployeeTypeAdmin(admin.ModelAdmin):
    list_display = ('type_id', 'name', 'price', 'status',)
    list_filter = ('status',)


class EmployeeGroupAdmin(admin.ModelAdmin):
    list_display = ('group_id', 'dingding_id', 'gender', 'status',)


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeType, EmployeeTypeAdmin)
admin.site.register(EmployeeGroup, EmployeeGroupAdmin)