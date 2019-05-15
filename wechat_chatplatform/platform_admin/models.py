# -*- coding: utf-8 -*-

from django.db import models
from django.utils.timezone import now

from wechat_chatplatform.common.choices import AdminUserStatus, Status


class AdminUser(models.Model):

    admin_user_id = models.AutoField(verbose_name=u'管理员编号', primary_key=True)
    username = models.CharField(verbose_name=u'姓名', max_length=20)
    password = models.CharField(verbose_name=u'密码', max_length=100)
    nickname = models.CharField(verbose_name=u'昵称', max_length=30)
    type_id = models.ForeignKey('platform_admin.AdminUserType', verbose_name=u'等级', related_name='type', on_delete=models.SET_NULL)
    status = models.IntegerField(verbose_name=u'状态', choices=AdminUserStatus.AdminUserStatusChoice.value, default=AdminUserStatus.active.value)
    mobile = models.CharField(verbose_name=u'联系电话', max_length=20)
    dingtalk_id = models.CharField(verbose_name=u'钉钉', max_length=30, null=True)
    dingtalk_robot = models.CharField(verbose_name=u'钉钉个人机器人', max_length=100, null=True)
    wechat_id = models.CharField(verbose_name=u'微信', max_length=30)
    join_date = models.DateField(verbose_name=u'入职日期', blank=True, null=True)
    leave_date = models.DateField(verbose_name=u'离职日期', blank=True, null=True)

    class Meta:
        db_table = 'admin_user'
        verbose_name = u'管理员用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname

    def delete(self, using=None, keep_parents=False):
        self.status = AdminUserStatus.leave.value
        self.leave_date = now().date()
        self.save()


class AdminUserType(models.Model):
    admin_user_type_id = models.AutoField(verbose_name=u'管理员等级编号', primary_key=True)
    name = models.CharField(verbose_name=u'等级', max_length=20)
    status = models.IntegerField(verbose_name=u'状态', choices=Status.StatusChoice.value, default=Status.active.value)

    class Meta:
        db_table = 'admin_user_type'
        verbose_name = u'管理员用户dengji '
        verbose_name_plural = verbose_name
