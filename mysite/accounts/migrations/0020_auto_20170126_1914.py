# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-26 19:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20170126_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_key',
            field=models.CharField(default='qxWsuHwYEHr6J9T6KtVM6gCFPXhU7keT4VFahwuV6eyb53etAQFvX54HegVj5rBE3n94vrmcWw4yDNRG6uFgXVPK8fBmjTUJ6Frt', max_length=100, verbose_name='用户key'),
        ),
    ]