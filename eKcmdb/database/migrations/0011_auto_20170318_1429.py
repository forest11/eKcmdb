# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-18 14:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0010_auto_20170318_1428'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sqlcheck',
            old_name='sqlsql_content',
            new_name='sql_content',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_key',
            field=models.CharField(default='rYmTCAxdYQFC9jAS7yh9eYRFkgSMhpgt6YFYTqvsE7xVWddWP3s4fdppjhF5SgABe9xYX87SbdPRv3cyKFdefhxCnWhaK9cQvU4Y', max_length=100, verbose_name='用户key'),
        ),
    ]
