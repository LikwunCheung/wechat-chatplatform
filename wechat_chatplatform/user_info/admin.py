# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import UserInfo, UserLoginInfo


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'open_id', 'name', 'last_login')
    empty_value_display = 'N/A'


class UserLoginInfoAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'time')
    empty_value_display = 'N/A'


admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(UserLoginInfo, UserLoginInfoAdmin)