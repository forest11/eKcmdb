# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-15 13:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20170115_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_key',
            field=models.CharField(default='bVAFygkGACvyQ8fTjwvCYKqBw3PEVRB8Myh4KJJXqQvRgAtJCBAQur7PGqEmn4YRa7pgF9eDnjnkf5tpvsVx4HA3gydxgTEJNYJa', max_length=100, verbose_name='用户key'),
        ),
    ]
