# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from wechat_chatplatform.common.choices import Status


class ProductType(models.Model):

    type_id = models.AutoField(verbose_name=u'产品类型编号', primary_key=True)
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

    product_id = models.AutoField(verbose_name=u'产品编号', primary_key=True)
    type_id = models.ForeignKey('product.ProductType', verbose_name=u'产品类型', related_name='type', on_delete=models.CASCADE)
    name = models.CharField(verbose_name=u'产品名称', max_length=20)
    eng_name = models.CharField(verbose_name=u'产品英文名称', max_length=30, blank=True, null=True)
    time = models.FloatField(verbose_name=u'时长', default=1)
    # default_price = models.FloatField(verbose_name=u'默认价格')
    partition = models.FloatField(verbose_name=u'首单分成', default=0.5)
    partition_extend = models.FloatField(verbose_name=u'续单分成', default=0.6)
    status = models.BooleanField(verbose_name=u'状态', choices=Status.StatusChoice.value, default=Status.active.value)

    class Meta:
        db_table = 'product'
        verbose_name = u'产品信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.type_id.__str__() + ' - ' + self.name

    def delete(self, using=None, keep_parents=False):
        self.status = Status.inactive.value
        self.save()


class ProductAnchorType(models.Model):

    product_anchor_type_id = models.AutoField(verbose_name=u'产品-店员类型编号', primary_key=True)
    product_id = models.ForeignKey('product.Product', verbose_name=u'产品', related_name='product', on_delete=models.CASCADE)
    anchor_type_id = models.ForeignKey('anchor.AnchorType', verbose_name=u'店员类型', related_name='anchor_type', on_delete=models.CASCADE)
    price = models.FloatField(verbose_name=u'价格')
    status = models.BooleanField(verbose_name=u'状态', choices=Status.StatusChoice.value, default=Status.active.value)

    class Meta:
        db_table = 'product_anchor_type'
        verbose_name = u'产品-店员类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.product_id.__str__() + ' - ' + self.anchor_type_id.__str__()

    def delete(self, using=None, keep_parents=False):
        self.status = Status.inactive.value
        self.save()
