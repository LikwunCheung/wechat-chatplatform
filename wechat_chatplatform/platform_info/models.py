from django.db import models

from wechat_chatplatform.common.choices import Status


class PlatformInfo(models.Model):

    platform_info_id = models.AutoField(verbose_name=u'平台信息编号', primary_key=True)
    tag = models.CharField(verbose_name=u'标签', max_length=20)
    tag_cn = models.CharField(verbose_name=u'描述', max_length=40)
    content = models.TextField(verbose_name=u'内容', max_length=500)
    status = models.BooleanField(verbose_name=u'状态', choices=Status.StatusChoice.value, default=Status.active.value)

    class Meta:
        db_table = 'platform_info'
        verbose_name = u'平台信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag_cn

    def _delete(self):
        self.status = Status.inactive.value
        self.save()
