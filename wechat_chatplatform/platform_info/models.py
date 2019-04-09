from django.db import models


class PlatformInfo(models.Model):
    STATUS_CHOICES = (
        (False, u'停用'),
        (True, u'激活'),
    )

    platform_info_id = models.AutoField(verbose_name=u'平台信息编号', primary_key=True)
    tag = models.CharField(verbose_name=u'标签', max_length=20)
    tag_cn = models.CharField(verbose_name=u'描述', max_length=40)
    content = models.TextField(verbose_name=u'内容', max_length=200)
    status = models.BooleanField(verbose_name=u'状态', choices=STATUS_CHOICES, default=True)

    class Meta:
        db_table = 'platform_info'
        verbose_name = u'平台信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag_cn

    def _delete(self):
        self.status = self.STATUS_CHOICES[False]
        self.save()
