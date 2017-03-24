#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
from django.db import models


class CheckCode(models.Model):
    """
    验证码临时表
    """
    email = models.CharField(max_length=32, db_index=True)
    code = models.CharField(max_length=12)
    times = models.IntegerField(default=1)
    ctime = models.DateTimeField()


class Permission(models.Model):
    """
    权限表
    """
    caption = models.CharField(max_length=32, verbose_name="权限描述")
    code = models.CharField(max_length=64, verbose_name="url权限")
    method = models.CharField(max_length=16, null=True, blank=True, verbose_name="请求方法")
    kwargs = models.CharField(max_length=128, null=True, blank=True, verbose_name="其他参数")  #同一个url的同一个请求方法的put，del进行判断

    class Meta:
        unique_together = ('code', 'method')
        verbose_name = "用户权限"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.caption


class Role(models.Model):
    """
    角色表
    """
    name = models.CharField(max_length=32, unique=True, verbose_name="角色名")
    perm = models.ManyToManyField('Permission')

    class Meta:
        verbose_name = "用户角色"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name