# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import AdminUser, AdminUserType


class AdminUserAdmin(admin.ModelAdmin):
    list_display = ('admin_user_id', 'username', 'nickname', 'type_id', 'status')
    empty_value_display = 'N/A'


class AdminUserTypeAdmin(admin.ModelAdmin):
    list_display = ('admin_user_type_id', 'name', 'status')
    empty_value_display = 'N/A'


admin.site.register(AdminUser, AdminUserAdmin)
admin.site.register(AdminUserType, AdminUserTypeAdmin)
