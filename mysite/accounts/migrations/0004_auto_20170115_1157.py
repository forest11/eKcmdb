# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-15 11:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20161229_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_key',
            field=models.CharField(default='SY5hT9cNdtHVYNbVsNJjYBfQFhpSAd5G6X5HryQ5Aed4TETYeeaKQgAerFRcGU7dEDs5ECC4eTjyeD3ERa8TWNRGTCCRyB3Q6N7W', max_length=100, verbose_name='用户key'),
        ),
    ]
