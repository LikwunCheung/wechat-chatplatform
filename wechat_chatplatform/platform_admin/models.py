# -*- coding: utf-8 -*-

from django.db import models
from django.utils.timezone import now

from wechat_chatplatform.common.choices import AdminUserStatus, Status


class AdminUser(models.Model):

    admin_user_id = models.AutoField(verbose_name=u'管理员编号', primary_key=True)
    admin_user_type = models.ForeignKey('platform_admin.AdminUserType', verbose_name=u'等级', related_name='admin_users', on_delete=models.SET_NULL, blank=True, null=True)
    username = models.CharField(verbose_name=u'用户名', max_length=20, unique=True)
    password = models.CharField(verbose_name=u'密码', max_length=100)
    nickname = models.CharField(verbose_name=u'昵称', max_length=30, blank=True, null=True)
    mobile = models.CharField(verbose_name=u'联系电话', max_length=20, blank=True, null=True)
    dingtalk_moblie = models.CharField(verbose_name=u'钉钉手机号', max_length=30, blank=True, null=True)
    dingtalk_robot = models.CharField(verbose_name=u'钉钉个人机器人', max_length=100, blank=True, null=True)
    wechat_id = models.CharField(verbose_name=u'微信', max_length=30, blank=True, null=True)
    join_date = models.DateField(verbose_name=u'入职日期', blank=True, null=True)
    leave_date = models.DateField(verbose_name=u'离职日期', blank=True, null=True)
    status = models.IntegerField(verbose_name=u'状态', choices=AdminUserStatus.AdminUserStatusChoice.value, default=AdminUserStatus.active.value)

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
    tag = models.CharField(verbose_name=u'标签', max_length=10, blank=True, null=True)
    status = models.BooleanField(verbose_name=u'状态', choices=Status.StatusChoice.value, default=Status.active.value)

    class Meta:
        db_table = 'admin_user_type'
        verbose_name = u'管理员用户等级'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        self.status = Status.inactive.value
        self.save()

