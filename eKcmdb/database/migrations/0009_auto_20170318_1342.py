# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-18 13:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0008_auto_20170315_1823'),
    ]

    operations = [
        migrations.CreateModel(
            name='SqlCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='名称')),
                ('sql', models.TextField(verbose_name='sql语句')),
                ('sql_result', models.TextField(verbose_name='sql执行结果')),
            ],
            options={
                'verbose_name': 'Sql检测',
                'verbose_name_plural': 'Sql检测',
            },
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_key',
            field=models.CharField(default='Wcc3NHuHyDhdHcUP8bT5HFKctsrRBGgBkYk4NqpYpcFnGWkg88CPsrJQCRGUEmG88S8tFrNXMTxmcrPmrNwhv5GGUdTsqVynCtAY', max_length=100, verbose_name='用户key'),
        ),
        migrations.AddField(
            model_name='sqlcheck',
            name='pusher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='申请人'),
        ),
    ]
