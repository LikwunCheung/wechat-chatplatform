# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math

from django.db import models
from django.utils.timezone import now

from wechat_chatplatform.common.choices import OrderStatus, Gender


class Order(models.Model):

    order_id = models.AutoField(verbose_name=u'订单编号', primary_key=True)
    user_id = models.ForeignKey('user_info.UserInfo', verbose_name=u'用户id', related_name='user', on_delete=models.SET_NULL, blank=True, null=True)
    product_id = models.ForeignKey('product.ProductAnchorType', verbose_name=u'产品', related_name='product', on_delete=models.SET_NULL, blank=True, null=True)
    anchor_id = models.ForeignKey('anchor.Anchor', verbose_name=u'雇员', related_name='anchor', on_delete=models.SET_NULL, blank=True, null=True)
    gender = models.IntegerField(verbose_name=u'性别', choices=Gender.GenderChoices.value, blank=True, null=True)
    status = models.IntegerField(verbose_name=u'状态', choices=OrderStatus.OrderStatusChoices.value, default=OrderStatus.unpaid.value)
    number = models.FloatField(verbose_name=u'件数', default=1)
    comment = models.CharField(verbose_name=u'备注', max_length=100, blank=True, null=True)
    origin_amount = models.FloatField(verbose_name=u'原金额')
    deduction = models.FloatField(verbose_name=u'折扣金额', default=0)
    total_amount = models.FloatField(verbose_name=u'总金额')
    rmb_amount = models.FloatField(verbose_name=u'人民币金额')
    order_time = models.DateTimeField(verbose_name=u'下单时间')
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
        self.status = OrderStatus.delete.value
        self.complete_time = now()
        self.save()

    def pay_salary(self):
        if self.status == OrderStatus.salary.value:
            self.status = OrderStatus.close.value
            self.salary_time = now()
            self.save()
        return None
