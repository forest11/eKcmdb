# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-15 13:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20170115_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_key',
            field=models.CharField(default='AtwCW7axBxM3gtcXcc57T86NCVbw8CMwkrT8TCQqqw4rgfv7bJgeU6u86CckJR9t8EaW9CayU6MPjFNEQy9EAvHKumYM6D8YHSgY', max_length=100, verbose_name='用户key'),
        ),
    ]