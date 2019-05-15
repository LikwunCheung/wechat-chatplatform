# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Anchor, AnchorType, AnchorGroup, AnchorCity, AnchorTag

# Register your models here.
admin.site.site_header = u'后台管理系统'
admin.site.site_title = u'后台管理系统'


class AnchorAdmin(admin.ModelAdmin):
    list_display = ('anchor_id', 'name', 'nickname', 'gender', 'age', 'constellation', 'type_id', 'mobile', 'status')
    list_filter = ('type_id', 'gender', 'status')
    search_fields = ('name', 'nickname',)
    exclude = ('age', 'status',)
    empty_value_display = 'N/A'


class AnchorTypeAdmin(admin.ModelAdmin):
    list_display = ('type_id', 'name', 'status',)
    list_filter = ('status',)


class AnchorGroupAdmin(admin.ModelAdmin):
    list_display = ('group_id', 'dingding_id', 'gender', 'status',)


class AnchorCityAdmin(admin.ModelAdmin):
    list_display = ('city_id', 'name', 'status',)
    list_filter = ('status',)


class AnchorTagAdmin(admin.ModelAdmin):
    list_display = ('tag_id', 'name', 'status',)
    list_filter = ('status',)


admin.site.register(Anchor, AnchorAdmin)
admin.site.register(AnchorType, AnchorTypeAdmin)
admin.site.register(AnchorTag, AnchorTagAdmin)
admin.site.register(AnchorCity, AnchorCityAdmin)
admin.site.register(AnchorGroup, AnchorGroupAdmin)
