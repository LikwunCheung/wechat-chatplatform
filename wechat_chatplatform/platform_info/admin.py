# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import PlatformInfo


class PlatformInfoAdmin(admin.ModelAdmin):
    list_display = ('tag', 'tag_cn', 'content', 'status')
    empty_value_display = 'N/A'


admin.site.register(PlatformInfo, PlatformInfoAdmin)