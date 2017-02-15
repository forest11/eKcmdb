# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-15 20:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0004_auto_20170215_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disk',
            name='slot',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='插槽位'),
        ),
        migrations.AlterField(
            model_name='manufactory',
            name='name',
            field=models.CharField(max_length=64, unique=True, verbose_name='制造厂商'),
        ),
        migrations.AlterField(
            model_name='ram',
            name='slot',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='插槽'),
        ),
    ]
