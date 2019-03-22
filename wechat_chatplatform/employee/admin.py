# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Employee, EmployeeType, EmployeeGroup, EmployeeCity, EmployeeTag

# Register your models here.
admin.site.site_header = u'后台管理系统'
admin.site.site_title = u'后台管理系统'


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'name', 'nickname', 'gender', 'age', 'type_id', 'mobile', 'status')
    list_filter = ('type_id', 'gender', 'status')
    search_fields = ('name', 'nickname',)
    exclude = ('age', 'status',)
    empty_value_display = 'N/A'


class EmployeeTypeAdmin(admin.ModelAdmin):
    list_display = ('type_id', 'name', 'status',)
    list_filter = ('status',)


class EmployeeGroupAdmin(admin.ModelAdmin):
    list_display = ('group_id', 'dingding_id', 'gender', 'status',)


class EmployeeCityAdmin(admin.ModelAdmin):
    list_display = ('city_id', 'name', 'status',)
    list_filter = ('status',)


class EmployeeTagAdmin(admin.ModelAdmin):
    list_display = ('tag_id', 'name', 'status',)
    list_filter = ('status',)


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeType, EmployeeTypeAdmin)
admin.site.register(EmployeeTag, EmployeeTagAdmin)
admin.site.register(EmployeeCity, EmployeeCityAdmin)
admin.site.register(EmployeeGroup, EmployeeGroupAdmin)
