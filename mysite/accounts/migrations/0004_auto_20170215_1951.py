# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-15 19:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20170212_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='code',
            field=models.CharField(default=18210000000, max_length=64, verbose_name='url权限'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='mobile',
            field=models.CharField(default=18210000000, max_length=32, verbose_name='手机'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_key',
            field=models.CharField(default='9QVSer5GqE5F9UPdffEdSkknFpahXPCkPSr9qMr8PJ3xDkVWT8XFJJ5mTE96uwgtbTBUmhnUVCE5queggvNtXcMmu6NqG8q89NAD', max_length=100, verbose_name='用户key'),
        ),
    ]