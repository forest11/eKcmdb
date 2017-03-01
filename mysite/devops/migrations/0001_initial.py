# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-12 15:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BindHost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Host')),
            ],
            options={
                'verbose_name': '主机与帐号绑定',
                'verbose_name_plural': '主机与帐号绑定',
            },
        ),
        migrations.CreateModel(
            name='HostGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('memo', models.CharField(blank=True, max_length=128, null=True)),
                ('bind_hosts', models.ManyToManyField(blank=True, to='devops.BindHost')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '主机组',
                'verbose_name_plural': '主机组',
            },
        ),
        migrations.CreateModel(
            name='RemoteUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auth_type', models.SmallIntegerField(choices=[(0, 'ssh-password'), (1, 'ssh-key')], default=0)),
                ('username', models.CharField(max_length=128)),
                ('password', models.CharField(help_text='如果auth_type选择为ssh-key,那此处就应该是key的路径', max_length=256)),
            ],
            options={
                'verbose_name': '远程用户',
                'verbose_name_plural': '远程用户',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_type', models.SmallIntegerField(choices=[(0, 'cmd'), (1, 'file_transfer')], verbose_name='执行类型')),
                ('task_detail', models.CharField(max_length=512)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('bind_hosts', models.ManyToManyField(to='devops.BindHost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='堡垒机账号')),
            ],
            options={
                'verbose_name': '任务',
                'verbose_name_plural': '任务',
            },
        ),
        migrations.CreateModel(
            name='TaskDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(choices=[('Success', 'Success'), ('Failed', 'Failed'), ('Processing', 'Processing'), ('Canceled', 'Canceled')], default='Processing', max_length=32, verbose_name='执行状态')),
                ('event_log', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('bind_host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devops.BindHost')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devops.Task')),
            ],
            options={
                'verbose_name': '任务日志',
                'verbose_name_plural': '任务日志',
            },
        ),
        migrations.AlterUniqueTogether(
            name='remoteuser',
            unique_together=set([('auth_type', 'username', 'password')]),
        ),
        migrations.AddField(
            model_name='bindhost',
            name='remote_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devops.RemoteUser'),
        ),
        migrations.AddField(
            model_name='bindhost',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='taskdetail',
            unique_together=set([('task', 'bind_host')]),
        ),
        migrations.AlterUniqueTogether(
            name='bindhost',
            unique_together=set([('host', 'remote_user')]),
        ),
    ]
