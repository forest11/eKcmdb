# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-27 08:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_auto_20170127_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_key',
            field=models.CharField(default='pYPrVyTDynJNYyNYggDCqaYXhnBskryFQe9RXwUpeEKByjP9RCYG6Jdf8kSCdJr8r7UqXHbXMXYKwMcd3j9qrUD8PtUF5qRaxMNg', max_length=100, verbose_name='用户key'),
        ),
    ]
