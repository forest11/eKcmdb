# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-15 12:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20170115_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_key',
            field=models.CharField(default='uDfcwn3tu94pGqxsUsXFaphvYjmWuVfNrwptjEfBDTNJCQtBFm7wUktUXxdjMxTHnRx8sDjDMpDQPQxSpw5f49qjcP3H9yNTEfya', max_length=100, verbose_name='用户key'),
        ),
    ]
