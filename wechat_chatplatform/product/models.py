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
    name = models.CharField(verbose_name=u'产品类型名称', max_length=20)
    eng_name = models.CharField(verbose_name=u'产品类型英文名称', max_length=30, blank=True, null=True)
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

    EXTEND_CHOICES = (
        (False, u'首单'),
        (True, u'续单'),
    )

    product_id = models.AutoField(verbose_name=u'产品编号', primary_key=True)
    type_id = models.ForeignKey('product.ProductType', verbose_name=u'产品类型', related_name='type', on_delete=models.CASCADE)
    name = models.CharField(verbose_name=u'产品名称', max_length=20)
    eng_name = models.CharField(verbose_name=u'产品英文名称', max_length=30, blank=True, null=True)
    time = models.FloatField(verbose_name=u'时长', default=1)
    price = models.FloatField(verbose_name=u'价格')
    partition = models.FloatField(verbose_name=u'首单分成', default=0.5)
    partition_extend = models.FloatField(verbose_name=u'续单分成', default=0.6)
    status = models.BooleanField(verbose_name=u'状态', choices=STATUS_CHOICES, default=True)

    class Meta:
        db_table = 'product'
        verbose_name = u'产品信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        self.status = self.STATUS_CHOICES[False]
        self.save()


class ProductEmployeeType(models.Model):

    STATUS_CHOICES = (
        (False, u'停用'),
        (True, u'激活'),
    )

    product_employee_type_id = models.AutoField(verbose_name=u'产品-雇员类型编号', primary_key=True)
    product_id = models.ForeignKey('product.Product', verbose_name=u'产品', related_name='product', on_delete=models.CASCADE)
    employee_type_id = models.ForeignKey('employee.EmployeeType', verbose_name=u'雇员类型', related_name='employee_type', on_delete=models.CASCADE)
