# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-15 19:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0003_auto_20170212_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='host',
            field=models.ManyToManyField(to='assets.Host'),
        ),
    ]