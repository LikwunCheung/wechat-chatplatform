# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math

from django.db import models
from django.utils.timezone import now


class Order(models.Model):
    STATUS_CHOICES = (
        (0, u'已删除'),
        (1, u'待付款'),
        (2, u'待接单'),
        (3, u'待抢单'),
        (4, u'待发放工资'),
        (5, u'正常关闭'),
        (6, u'已换人'),
        (7, u'付款超时失败')
    )

    order_id = models.AutoField(verbose_name=u'订单编号', primary_key=True)
    # user_id = models.ForeignKey('user_info.UserInfo', verbose_name=u'用户id', related_name='user', on_delete=models.SET_NULL, blank=True, null=True)
    product_id = models.ForeignKey('product.ProductEmployeeType', verbose_name=u'产品', related_name='product', on_delete=models.SET_NULL, blank=True, null=True)
    employee_id = models.ForeignKey('employee.Employee', verbose_name=u'雇员', related_name='employee', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.IntegerField(verbose_name=u'状态', choices=STATUS_CHOICES, default=1)
    number = models.FloatField(verbose_name=u'件数', default=1)
    origin_amount = models.FloatField(verbose_name=u'原金额')
    deduction = models.FloatField(verbose_name=u'折扣金额', default=0)
    total_amount = models.FloatField(verbose_name=u'总金额')
    rmb_amount = models.FloatField(verbose_name=u'人民币金额')
    order_time = models.DateTimeField(verbose_name=u'下单时间', default=now())
    pay_time = models.DateTimeField(verbose_name=u'付款时间', blank=True, null=True)
    complete_time = models.DateTimeField(verbose_name=u'完成时间', blank=True, null=True)
    salary_time = models.DateTimeField(verbose_name=u'工资结算时间', blank=True, null=True)

    class Meta:
        db_table = 'order'
        verbose_name = u'订单信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_id.__str__()

    def _delete(self):
        if self.pay_time or self.complete_time or self.salary_time:
            return None
        self.status = self.STATUS_CHOICES[0]
        self.complete_time = now()
        self.save()

    def pay_salary(self):
        if self.status == 4:
            self.status = 5
            self.salary_time = now()
            self.save()
        return None
