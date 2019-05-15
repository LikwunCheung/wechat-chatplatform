# Generated by Django 2.2 on 2019-05-10 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_auto_20190322_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.IntegerField(choices=[(0, '女'), (1, '男'), (2, '混合')], verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='status',
            field=models.IntegerField(choices=[(0, '离职'), (1, '在职'), (2, '待审核'), (3, '审核失败')], default=2, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='employeecity',
            name='status',
            field=models.BooleanField(choices=[(False, '失效'), (True, '激活')], default=True, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='employeegroup',
            name='gender',
            field=models.IntegerField(choices=[(0, '女'), (1, '男'), (2, '混合')], default=2, verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='employeegroup',
            name='status',
            field=models.BooleanField(choices=[(False, '失效'), (True, '激活')], default=True, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='employeetag',
            name='status',
            field=models.BooleanField(choices=[(False, '失效'), (True, '激活')], default=True, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='employeetype',
            name='status',
            field=models.BooleanField(choices=[(False, '失效'), (True, '激活')], default=True, verbose_name='状态'),
        ),
    ]