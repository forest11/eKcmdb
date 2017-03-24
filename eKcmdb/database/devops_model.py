#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
from django.db import models


class RemoteUser(models.Model):
    """主机用户"""
    auth_type_choices = (
        (0, 'ssh-password'),
        (1, 'ssh-key')
    )
    auth_type = models.SmallIntegerField(choices=auth_type_choices, default=0)
    username = models.CharField(max_length=128, verbose_name="远程主机账号")
    password = models.CharField(max_length=256, help_text="如果auth_type选择为ssh-key,那此处就应该是key的路径")

    def __str__(self):
        return self.username

    class Meta:
        unique_together = ('auth_type', 'username', 'password')
        verbose_name = "远程主机账号"
        verbose_name_plural = verbose_name


class BindHost(models.Model):
    """
    主机与系统账号绑定
    """
    host = models.ForeignKey('Host')
    user = models.ManyToManyField('UserProfile', related_name="h", blank=True)
    port = models.IntegerField(default=22)
    remote_user = models.ForeignKey(RemoteUser)

    def __str__(self):
        return "%s:%s" % (self.host.hostname, self.remote_user.username)

    class Meta:
        unique_together = ('host', 'remote_user')
        verbose_name = "主机与系统账号绑定"
        verbose_name_plural = verbose_name


class HostGroups(models.Model):
    """
    主机组
    """
    name = models.CharField(max_length=64, unique=True, verbose_name="名称")
    user = models.ManyToManyField('UserProfile', related_name="g", blank=True)
    bind_hosts = models.ManyToManyField('BindHost', blank=True)
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name="备注")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "主机组"
        verbose_name_plural = verbose_name


class Task(models.Model):
    """
    任务
    """
    action_choices = (
        (0, 'cmd'),
        (1, 'file_transfer')
    )
    task_type = models.SmallIntegerField(choices=action_choices, verbose_name="执行类型")
    user = models.ForeignKey('UserProfile', verbose_name='堡垒机账号')
    bind_hosts = models.ManyToManyField('BindHost', related_name='t', blank=True)
    cmd = models.CharField(max_length=512, verbose_name="命令日志")

    def __str__(self):
        return "%s: %s" % (self.user.name, self.cmd)

    class Meta:
        verbose_name = "CMD任务"
        verbose_name_plural = verbose_name


class TaskDetail(models.Model):
    """
    任务日志
    """
    bing_task = models.ForeignKey('Task')
    task_result_choices = (
        (0, '正在执行'),
        (1, '执行成功'),
        (2, '执行失败'),
        (3, '未知')
    )
    exec_status = models.SmallIntegerField(choices=task_result_choices, default=3, verbose_name="执行状态")
    bind_host = models.ForeignKey('BindHost', related_name='d', blank=True)
    event_log = models.TextField()
    task_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.bing_task.cmd

    class Meta:
        unique_together = ('bing_task', 'bind_host')
        verbose_name = "任务日志"
        verbose_name_plural = verbose_name


class Code(models.Model):
    """
    代码发布
    """
    status_choices = (
        (0, "等待发布中"),
        (1, "等待测试中"),
        (2, "已完成"),
        (3, "测试失败"),
        (4, "未知"),
    )
    step_choices = (
        (1, "发布申请"),
        (2, "灰度发布"),
        (3, "灰度测试"),
        (4, "生产发布"),
        (5, "生产测试"),
        (6, "代码合并"),
    )
    name = models.CharField(max_length=256, unique=True, verbose_name="发布名称")
    version = models.CharField(max_length=32, verbose_name="版本号")
    content = models.TextField(verbose_name="发布内容")
    env = models.ForeignKey("Environment", verbose_name="发布环境")
    project = models.ForeignKey('BusinessUnit', verbose_name="项目名")
    pusher = models.ForeignKey('UserProfile', related_name="p", blank=True, verbose_name="发布者")
    commit_time = models.DateTimeField(auto_now_add=True, verbose_name="提交时间")
    hd_tester = models.ManyToManyField('UserProfile', related_name="t", blank=True, verbose_name="灰度测试者")
    hd_mome = models.TextField(verbose_name="灰度备注")
    hd_time = models.DateTimeField(auto_now_add=True, verbose_name="灰度测试完成时间")
    production_tester = models.ManyToManyField('UserProfile', related_name="r", blank=True, verbose_name="生产测试者")
    production_mome = models.TextField(verbose_name="生产备注")
    production_time = models.DateTimeField(auto_now_add=True, verbose_name="生产测试完成时间")
    approve_time = models.DateTimeField(null=True, blank=True, verbose_name="代码合并时间")
    status = models.SmallIntegerField(choices=status_choices, default=4, verbose_name="发布状态")
    steps = models.SmallIntegerField(choices=step_choices, default=1, verbose_name="当前步骤")


class Environment(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name="名称")
    memo = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "运行环境"
        verbose_name_plural = verbose_name


class CodeLog(models.Model):
    log = models.TextField(verbose_name="log")

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = "发布日志"
        verbose_name_plural = verbose_name


class SqlCheck(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name="名称")
    pusher = models.ForeignKey('UserProfile',  verbose_name="申请人")
    sql_content = models.TextField(verbose_name="sql语句")
    sql_result = models.TextField(null=True, blank=True, verbose_name="sql执行结果")
    exec_time = models.DateTimeField(auto_now_add=True, verbose_name="时间")

    def __str__(self):
        return self.sql

    class Meta:
        verbose_name = "SQL检查"
        verbose_name_plural = verbose_name


class UrlCenter(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name="名称")
    url = models.URLField(verbose_name="名称")
    memo = models.CharField(max_length=256, verbose_name="说明")

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = "url管理中心"
        verbose_name_plural = verbose_name