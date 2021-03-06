# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Product, ProductType, ProductAnchorType


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('product_type_id', 'name', 'status',)
    list_filter = ('status',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_type', 'name', 'time', 'partition', 'partition_extend', 'status',)
    list_filter = ('product_type', 'status',)
    empty_value_display = 'N/A'


class ProductAnchorTypeAdmin(admin.ModelAdmin):
    list_display = ('product_anchor_type_id', 'product', 'anchor_type', 'price', 'status',)
    list_filter = ('product', 'anchor_type', 'status',)


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(ProductAnchorType, ProductAnchorTypeAdmin)
