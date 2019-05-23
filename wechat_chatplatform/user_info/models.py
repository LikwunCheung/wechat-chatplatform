# -*- coding: utf-8 -*-

import base64

from django.db import models

from wechat_chatplatform.common.choices import Gender


class UserInfo(models.Model):

    user_id = models.AutoField(verbose_name=u'用户编号', primary_key=True)
    open_id = models.CharField(verbose_name=u'微信开放编号', max_length=60, blank=True, null=True)
    nickname = models.CharField(verbose_name=u'用户昵称', max_length=20, blank=True, null=True)
    access_token = models.CharField(verbose_name=u'Token', max_length=150, blank=True, null=True)
    avatar = models.CharField(verbose_name=u'用户头像', max_length=150, blank=True, null=True)
    gender = models.IntegerField(verbose_name=u'性别', choices=Gender.GenderChoices.value, default=0)
    last_login = models.DateTimeField(verbose_name=u'最后登入时间', blank=True, null=True)

    class Meta:
        db_table = 'user_info'
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname

    def name(self):
        nickname = str(base64.b64decode(self.nickname), 'utr8')
        return nickname

    name.short_description = u'昵称'

    def save_nickname(self, nickname):
        self.nickname = str(base64.b64encode(nickname.encode('utf8')), 'utf8')


class UserLoginInfo(models.Model):
    user_login_id = models.AutoField(verbose_name=u'用户登入编号', primary_key=True)
    user = models.ForeignKey('user_info.UserInfo', verbose_name=u'用户', related_name='logins', on_delete=models.SET_NULL, blank=True, null=True)
    time = models.DateTimeField(verbose_name=u'时间')

    class Meta:
        db_table = 'user_login_info'
        verbose_name = u'用户登陆日志'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.nickname
