#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
from django import forms
from database import models
from django.core.exceptions import ValidationError


class BusinessForm(forms.ModelForm):
    """
    业务线
    """
    class Meta:
        model = models.BusinessUnit
        exclude = ("id",)

    def save(self, commit=True):
        business = super(BusinessForm, self).save(commit=False)
        if commit:
            business.save()
        return business


class ServiceForm(forms.ModelForm):
    """
    服务
    """
    class Meta:
        model = models.Service
        exclude = ("id",)


class SQLCheck(forms.ModelForm):
    """
    sql检测
    """
    class Meta:
        model = models.SqlCheck
        exclude = ("id", "pusher", "sql_result", "exec_time")
