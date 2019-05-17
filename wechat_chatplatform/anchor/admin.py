# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Anchor, AnchorType, AnchorGroup, AnchorTag, AnchorApplyRecord

# Register your models here.
admin.site.site_header = u'后台管理系统'
admin.site.site_title = u'后台管理系统'


class AnchorAdmin(admin.ModelAdmin):
    list_display = ('anchor_id', 'nickname', 'gender', 'age', 'constellation', 'type_id', 'status')
    list_filter = ('type_id', 'gender', 'status')
    search_fields = ('name', 'nickname',)
    empty_value_display = 'N/A'


class AnchorTypeAdmin(admin.ModelAdmin):
    list_display = ('type_id', 'name', 'status',)
    list_filter = ('status',)


class AnchorGroupAdmin(admin.ModelAdmin):
    list_display = ('group_id', 'dingtalk_robot', 'gender', 'status',)


class AnchorTagAdmin(admin.ModelAdmin):
    list_display = ('tag_id', 'name', 'status',)
    list_filter = ('status',)


class AnchorApplyRecordAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'gender', 'city', 'birthday', 'status', 'apply_date')
    list_filter = ('status',)


admin.site.register(Anchor, AnchorAdmin)
admin.site.register(AnchorType, AnchorTypeAdmin)
admin.site.register(AnchorTag, AnchorTagAdmin)
admin.site.register(AnchorGroup, AnchorGroupAdmin)
admin.site.register(AnchorApplyRecord, AnchorApplyRecordAdmin)
