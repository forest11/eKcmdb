#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
from django import forms
from assets import models
from django.core.exceptions import ValidationError


class BusinessForm(forms.ModelForm):
    class Meta:
        model = models.BusinessUnit
        exclude = ("id",)

    def clean_service(self):
        service = self.cleaned_data.get('service')
        if not service:
            service = None
        return service


class UpdateBusinessForm(forms.Form):
    id = forms.CharField(required=True, error_messages={'required': '业务线id不能为空'})
    name = forms.CharField(required=True, error_messages={'required': '业务线名不能为空'})
    service = forms.CharField(required=False)
    memo = forms.CharField(required=False)


class ServiceForm(forms.ModelForm):
    class Meta:
        model = models.Service
        exclude = ("id",)

    def clean_host(self):
        host = self.cleaned_data.get('host')
        if not host:
            host = None
        return host


class UpdateServiceForm(forms.Form):
    class Meta:
        model = models.Service
        field = ("id", "port", "host", "name", "memo")

    def clean_host(self):
        host = self.cleaned_data.get('host')
        if not host:
            host = None
        return host