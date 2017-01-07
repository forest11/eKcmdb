# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-28 10:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False, verbose_name='管理员')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('token', models.CharField(blank=True, max_length=128, null=True, verbose_name='用户token')),
                ('user_key', models.CharField(default='xRX5Mx5q8B77pPvHHMmqPQ3DdqeMUvajVTNfwgna65WKt7sWaAeskyshdkbHWhsS6hpsNvhWanwD4KUdd7RbuSFYAGWA9bn9JbWr', max_length=100, verbose_name='用户key')),
                ('department', models.CharField(blank=True, max_length=32, null=True, verbose_name='部门')),
                ('tel', models.CharField(blank=True, max_length=32, null=True, verbose_name='座机')),
                ('mobile', models.CharField(blank=True, max_length=32, null=True, verbose_name='手机')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
            },
        ),
        migrations.CreateModel(
            name='CheckCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(db_index=True, max_length=32)),
                ('code', models.CharField(max_length=12)),
                ('times', models.IntegerField(default=1)),
                ('ctime', models.DateTimeField()),
            ],
        ),
    ]
