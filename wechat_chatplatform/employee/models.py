# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math

from django.db import models
from django.utils.timezone import now

from wechat_chatplatform.common.choices import IdentityType, EmployeeStatus, Gender, Status


class Employee(models.Model):

    employee_id = models.AutoField(verbose_name=u'雇员编号', primary_key=True)
    name = models.CharField(verbose_name=u'姓名', max_length=20)
    nickname = models.CharField(verbose_name=u'昵称', max_length=30)
    type_id = models.ForeignKey('employee.EmployeeType', verbose_name=u'等级', related_name='type', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.IntegerField(verbose_name=u'状态', choices=EmployeeStatus.EmployeeStatusChoice.value, default=2)
    city_id = models.ForeignKey('employee.EmployeeCity', verbose_name=u'城市', related_name='city', on_delete=models.SET_NULL, blank=True, null=True)
    identity_type = models.IntegerField(verbose_name=u'证件类型', choices=IdentityType.IdentityTypeChoice.value, default=0)
    identity = models.CharField(verbose_name=u'证件号码', max_length=20)
    birthday = models.DateField(verbose_name=u'生日')
    gender = models.IntegerField(verbose_name=u'性别', choices=Gender.GenderChoices.value)
    mobile = models.CharField(verbose_name=u'联系电话', max_length=20)
    dingtalk_id = models.CharField(verbose_name=u'钉钉', max_length=30, blank=True, null=True)
    dingtalk_robot = models.CharField(verbose_name=u'钉钉个人机器人', max_length=100, blank=True, null=True)
    wechat_id = models.CharField(verbose_name=u'微信', max_length=30)
    audio = models.CharField(verbose_name=u'音频', max_length=100, blank=True, null=True)
    avatar = models.CharField(verbose_name=u'头像', max_length=100, blank=True, null=True)
    img1 = models.CharField(verbose_name=u'图片1', max_length=100, blank=True, null=True)
    img2 = models.CharField(verbose_name=u'图片2', max_length=100, blank=True, null=True)
    img3 = models.CharField(verbose_name=u'图片3', max_length=100, blank=True, null=True)
    audit_date = models.DateTimeField(verbose_name=u'审核时间', blank=True, null=True)
    auditor = models.ForeignKey('platform_admin.AdminUser', verbose_name=u'审核人', related_name='auditor', on_delete=models.SET_NULL, blank=True, null=True)
    join_date = models.DateField(verbose_name=u'入职日期', blank=True, null=True)
    leave_date = models.DateField(verbose_name=u'离职日期', blank=True, null=True)
    slogan = models.CharField(verbose_name=u'标语', max_length=150, null=True)
    tags = models.CharField(verbose_name=u'标签', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'employee'
        verbose_name = u'雇员信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def age(self):
        if not self.birthday:
            return 'N/A'
        return math.floor((now().date() - self.birthday).days / 365)

    age.short_description = u'年龄'

    def constellation(self):
        pass

    constellation.short_description = u'星座'

    def delete(self, using=None, keep_parents=False):
        self.status = EmployeeStatus.leave.value
        self.leave_date = now().date()
        self.save()

    def audit_pass(self):
        if self.status == EmployeeStatus.unaudit.value:
            self.status = EmployeeStatus.active.value
            self.join_date = now().date()
            self.save()
            return True
        return False

    def audit_reject(self):
        if self.status == EmployeeStatus.unaudit.value:
            self.status = EmployeeStatus.audit_fail.value
            self.save()
            return True
        return False


class EmployeeTag(models.Model):

    tag_id = models.AutoField(verbose_name=u'标签编号', primary_key=True)
    name = models.CharField(verbose_name=u'标签', max_length=15)
    status = models.BooleanField(verbose_name=u'状态', choices=Status.StatusChoice.value, default=Status.active.value)

    class Meta:
        db_table = 'employee_tag'
        verbose_name = u'雇员标签信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        self.status = Status.inactive.value
        self.save()


class EmployeeCity(models.Model):
    STATUS_CHOICES = (
        (Status.inactive.value, u'停用'),
        (Status.active.value, u'激活'),
    )

    city_id = models.AutoField(verbose_name=u'城市编号', primary_key=True)
    name = models.CharField(verbose_name=u'中文名', max_length=15)
    en_name = models.CharField(verbose_name=u'英文名', max_length=15, blank=True, null=True)
    status = models.BooleanField(verbose_name=u'状态', choices=Status.StatusChoice.value, default=Status.active.value)

    class Meta:
        db_table = 'employee_city'
        verbose_name = u'雇员城市信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        self.status = Status.inactive.value
        self.save()
    #
    # @staticmethod
    # def get_all_city():
    #     # return EmployeeCity.objects().all()
    #     pass


class EmployeeType(models.Model):
    STATUS_CHOICES = (
        (Status.inactive.value, u'停用'),
        (Status.active.value, u'激活'),
    )

    type_id = models.AutoField(verbose_name=u'雇员类型编号', primary_key=True)
    name = models.CharField(verbose_name=u'雇员类型', max_length=15)
    status = models.BooleanField(verbose_name=u'状态', choices=Status.StatusChoice.value, default=Status.active.value)

    class Meta:
        db_table = 'employee_type'
        verbose_name = u'雇员类型信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        self.status = Status.inactive.value
        self.save()


class EmployeeGroup(models.Model):
    GENDER_CHOICES = (
        (Gender.male.value, u'男'),
        (Gender.female.value, u'女'),
        (Gender.mix.value, u'混合'),
    )
    STATUS_CHOICES = (
        (Status.inactive.value, u'停用'),
        (Status.active.value, u'激活'),
    )

    group_id = models.AutoField(verbose_name=u'雇员钉钉群编号', primary_key=True)
    name = models.CharField(verbose_name=u'群名称', max_length=20)
    dingding_id = models.CharField(verbose_name=u'钉钉id', max_length=30)
    gender = models.IntegerField(verbose_name=u'性别', choices=Gender.GenderChoices.value, default=Gender.mix.value)
    status = models.BooleanField(verbose_name=u'状态', choices=Status.StatusChoice.value, default=Status.active.value)

    class Meta:
        db_table = 'employee_group'
        verbose_name = u'雇员群信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.dingding_id

    def delete(self, using=None, keep_parents=False):
        self.status = Status.inactive.value
        self.save()
