# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-27 08:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_auto_20170127_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_key',
            field=models.CharField(default='AT7v4uhS7bYRWXYCMujTASQQbn9jEjRF5vGTXjhswW6wUYM7PvmnyBAuqM6aUNhMrqrdCHV8gpGwbvEStT8FFqQBcxrY5EecQguR', max_length=100, verbose_name='用户key'),
        ),
    ]
