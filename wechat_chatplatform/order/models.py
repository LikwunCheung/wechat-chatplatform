# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math

from django.db import models
from django.utils.timezone import now

from wechat_chatplatform.common.choices import OrderStatus, Gender, OrderType, OrderRenew


class Order(models.Model):

    order_id = models.AutoField(verbose_name=u'订单编号', primary_key=True)
    order_type = models.IntegerField(verbose_name=u'订单类型', choices=OrderType.OrderTypeChoices.value, default=OrderType.normal.value, blank=True, null=True)
    renew = models.IntegerField(verbose_name=u'首续单', choices=OrderRenew.OrderRenewChoices.value, default=OrderRenew.first.value, blank=True, null=True)
    user = models.ForeignKey('user_info.UserInfo', verbose_name=u'用户', related_name='orders', on_delete=models.SET_NULL, blank=True, null=True)
    anchor = models.ForeignKey('anchor.Anchor', verbose_name=u'店员', related_name='orders', on_delete=models.SET_NULL, blank=True, null=True)
    anchor_type = models.ForeignKey('anchor.AnchorType', verbose_name=u'店员等级', related_name='orders', on_delete=models.SET_NULL, blank=True, null=True)
    product_anchor = models.ForeignKey('product.ProductAnchorType', verbose_name=u'产品', related_name='orders', on_delete=models.SET_NULL, blank=True, null=True)
    wechat_id = models.CharField(verbose_name=u'微信号', max_length=30, blank=True, null=True)
    gender = models.IntegerField(verbose_name=u'性别', choices=Gender.GenderChoices.value, blank=True, null=True)
    number = models.IntegerField(verbose_name=u'件数', default=1)
    comment = models.CharField(verbose_name=u'备注', max_length=100, blank=True, null=True)
    origin_amount = models.FloatField(verbose_name=u'原金额')
    deduction = models.FloatField(verbose_name=u'折扣金额', default=0)
    total_amount = models.FloatField(verbose_name=u'总金额')
    rmb_amount = models.FloatField(verbose_name=u'人民币金额')
    order_time = models.DateTimeField(verbose_name=u'下单时间', db_index=True)
    pay_time = models.DateTimeField(verbose_name=u'付款时间', blank=True, null=True, db_index=True)
    complete_time = models.DateTimeField(verbose_name=u'完成时间', blank=True, null=True, db_index=True)
    salary_time = models.DateTimeField(verbose_name=u'工资结算时间', blank=True, null=True, db_index=True)
    status = models.IntegerField(verbose_name=u'状态', choices=OrderStatus.OrderStatusChoices.value, default=OrderStatus.unpaid.value, db_index=True)

    class Meta:
        db_table = 'order'
        verbose_name = u'订单信息'
        verbose_name_plural = verbose_name
        indexes = []

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


class OrderHistory(models.Model):

    order_history_id = models.AutoField(verbose_name=u'订单记录编号', primary_key=True)
    date = models.DateField(verbose_name=u'日期', db_index=True)
    update_date = models.DateTimeField(verbose_name=u'更新时间', default=0)
    order_number = models.IntegerField(verbose_name=u'订单数量', default=0)
    order_amount = models.FloatField(verbose_name=u'订单金额', default=0)
    direct_order_number = models.IntegerField(verbose_name=u'指定单数量', default=0)
    direct_order_amount = models.FloatField(verbose_name=u'指定单金额', default=0)
    random_order_number = models.IntegerField(verbose_name=u'随机单数量', default=0)
    random_order_amount = models.FloatField(verbose_name=u'随机单金额', default=0)
    first_order_number = models.IntegerField(verbose_name=u'首单数量', default=0)
    first_order_amount = models.FloatField(verbose_name=u'首单金额', default=0)
    renew_order_number = models.IntegerField(verbose_name=u'续单数量', default=0)
    renew_order_amount = models.FloatField(verbose_name=u'续单金额', default=0)
    complete_number = models.IntegerField(verbose_name=u'结单数量', default=0)
    complete_amount = models.FloatField(verbose_name=u'结单金额', default=0)
    salary_number = models.IntegerField(verbose_name=u'发工资数量', default=0)
    salary_amount = models.FloatField(verbose_name=u'发工资金额', default=0)
    access_count = models.IntegerField(verbose_name=u'访问总量', default=0)
    distinct_access_count = models.IntegerField(verbose_name=u'访问用户数量', default=0)

    class Meta:
        db_table = 'order_history'
        verbose_name = u'订单统计'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')