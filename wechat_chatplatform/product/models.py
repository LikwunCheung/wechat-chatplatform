# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from wechat_chatplatform.common.choices import Status


class ProductType(models.Model):

    product_type_id = models.AutoField(verbose_name=u'产品类型编号', primary_key=True)
    name = models.CharField(verbose_name=u'产品类型名称', max_length=20)
    eng_name = models.CharField(verbose_name=u'产品类型英文名称', max_length=30, blank=True, null=True)
    status = models.BooleanField(verbose_name=u'状态', choices=Status.StatusChoice.value, default=Status.active.value)

    class Meta:
        db_table = 'product_type'
        verbose_name = u'产品类型信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        self.status = Status.inactive.value
        self.save()


class Product(models.Model):

    product_id = models.AutoField(verbose_name=u'时长编号', primary_key=True)
    product_type = models.ForeignKey('product.ProductType', verbose_name=u'产品类型', related_name='products', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(verbose_name=u'时长名称', max_length=20)
    eng_name = models.CharField(verbose_name=u'时长英文名称', max_length=30, blank=True, null=True)
    time = models.FloatField(verbose_name=u'具体时长', default=1)
    partition = models.FloatField(verbose_name=u'首单分成', default=0.5)
    partition_extend = models.FloatField(verbose_name=u'续单分成', default=0.6)
    status = models.BooleanField(verbose_name=u'状态', choices=Status.StatusChoice.value, default=Status.active.value)

    class Meta:
        db_table = 'product'
        verbose_name = u'产品-时长信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.product_type.__str__() + ' - ' + self.name

    def delete(self, using=None, keep_parents=False):
        self.status = Status.inactive.value
        self.save()


class ProductAnchorType(models.Model):

    product_anchor_type_id = models.AutoField(verbose_name=u'产品-时长-店员等级关系编号', primary_key=True)
    product = models.ForeignKey('product.Product', verbose_name=u'产品-时长', related_name='anchor_type', on_delete=models.CASCADE, blank=True, null=True)
    anchor_type = models.ForeignKey('anchor.AnchorType', verbose_name=u'店员类型', related_name='products', on_delete=models.CASCADE, blank=True, null=True)
    price = models.FloatField(verbose_name=u'价格')
    status = models.BooleanField(verbose_name=u'状态', choices=Status.StatusChoice.value, default=Status.active.value)

    class Meta:
        db_table = 'product_anchor_type'
        verbose_name = u'产品-时长-店员类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.product.__str__() + ' - ' + self.anchor_type.__str__()

    def delete(self, using=None, keep_parents=False):
        self.status = Status.inactive.value
        self.save()
