# Generated by Django 2.1.7 on 2019-05-15 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('admin_user_id', models.AutoField(primary_key=True, serialize=False, verbose_name='管理员编号')),
                ('username', models.CharField(max_length=20, verbose_name='姓名')),
                ('password', models.CharField(max_length=100, verbose_name='密码')),
                ('nickname', models.CharField(max_length=30, verbose_name='昵称')),
                ('status', models.IntegerField(choices=[(0, '离职'), (1, '在职')], default=1, verbose_name='状态')),
                ('mobile', models.CharField(max_length=20, verbose_name='联系电话')),
                ('dingtalk_id', models.CharField(max_length=30, null=True, verbose_name='钉钉')),
                ('dingtalk_robot', models.CharField(max_length=100, null=True, verbose_name='钉钉个人机器人')),
                ('wechat_id', models.CharField(max_length=30, verbose_name='微信')),
                ('join_date', models.DateField(blank=True, null=True, verbose_name='入职日期')),
                ('leave_date', models.DateField(blank=True, null=True, verbose_name='离职日期')),
            ],
            options={
                'verbose_name': '管理员用户',
                'verbose_name_plural': '管理员用户',
                'db_table': 'admin_user',
            },
        ),
        migrations.CreateModel(
            name='AdminUserType',
            fields=[
                ('admin_user_type_id', models.AutoField(primary_key=True, serialize=False, verbose_name='管理员等级编号')),
                ('name', models.CharField(max_length=20, verbose_name='等级')),
                ('status', models.IntegerField(choices=[(False, '失效'), (True, '激活')], default=True, verbose_name='状态')),
            ],
            options={
                'verbose_name': '管理员用户dengji ',
                'verbose_name_plural': '管理员用户dengji ',
                'db_table': 'admin_user_type',
            },
        ),
        migrations.AddField(
            model_name='adminuser',
            name='type_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='type', to='platform_admin.AdminUserType', verbose_name='等级'),
        ),
    ]
