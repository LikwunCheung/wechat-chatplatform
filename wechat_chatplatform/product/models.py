# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math

from django.db import models
from django.utils.timezone import now


class ProductType(models.Model):

    STATUS_CHOICES = (
        (False, u'停用'),
        (True, u'激活'),
    )

    type_id = models.AutoField(verbose_name=u'产品类型编号', primary_key=True)
    name = models.CharField(verbose_name=u'产品类型名', max_length=20)
    eng_name = models.CharField(verbose_name=u'产品英文名', max_length=30, blank=True, null=True)
    status = models.BooleanField(verbose_name=u'状态', choices=STATUS_CHOICES, default=True)

    class Meta:
        db_table = 'product_type'
        verbose_name = u'产品类型信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        self.status = self.STATUS_CHOICES[False]
        self.save()


class Product(models.Model):

    STATUS_CHOICES = (
        (False, u'停用'),
        (True, u'激活'),
    )

    type_id = models.AutoField(verbose_name=u'产品类型编号', primary_key=True)
    name = models.CharField(verbose_name=u'产品类型名', max_length=20)
    eng_name = models.CharField(verbose_name=u'产品英文名', max_length=30, blank=True, null=True)
    status = models.BooleanField(verbose_name=u'状态', choices=STATUS_CHOICES, default=True)

    class Meta:
        db_table = 'product_type'
        verbose_name = u'产品类型信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        self.status = self.STATUS_CHOICES[False]
        self.save()
