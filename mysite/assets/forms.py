# -*- coding: utf-8 -*-
# __Author__: PanDongLin
from django.core.exceptions import ValidationError
from django import forms
from assets import models


class HostAdd(forms.Form):
    sn = forms.CharField(required=True, error_messages={'required': 'sn不能为空'})
    number = forms.CharField(required=False)
    qs = forms.CharField(required=False)
    hostname = forms.CharField(required=True, error_messages={'required': '主机名不能为空'})
    asset_name = forms.CharField(required=False)
    manufactory = forms.CharField(required=False)
    management_ip = forms.GenericIPAddressField(required=False)
    is_virtual = forms.BooleanField(required=False)
    idc = forms.CharField(required=False)
    cabinet = forms.CharField(required=False)
    host_cabinet_id = forms.CharField(required=False)
    status = forms.CharField(required=False)
    buy_date = forms.DateField(required=False)
    memo = forms.CharField(required=False)


class HostEdit(forms.ModelForm):
    class Meta:
        model = models.Host
        exclude = ("id", "create_date")

    def clean_parent_host(self):
        parent_host = self.cleaned_data.get('parent_host')
        if not parent_host:
            parent_host = None
        return parent_host

    def clean_manufactory(self):
        manufactory = self.cleaned_data.get('manufactory')
        if not manufactory:
            manufactory = None
        return manufactory

    def clean_idc(self):
        idc = self.cleaned_data.get('idc')
        if not idc:
            idc = None
        return idc


# class HostEdit(forms.Form):
#     sn = forms.CharField(required=True, error_messages={'required': 'sn不能为空'})
#     number = forms.CharField(required=False)
#     qs = forms.CharField(required=False)
#     hostname = forms.CharField(required=True, error_messages={'required': '主机名不能为空'})
#     asset_name = forms.CharField(required=False)
#     os_type = forms.CharField(required=False)
#     manufactory = forms.CharField(required=False)
#     raid_type = forms.CharField(required=False)
#     management_ip = forms.GenericIPAddressField(required=False)
#     is_virtual = forms.BooleanField(required=False)
#     parent_host = forms.CharField(required=False)
#     idc = forms.CharField(required=False)
#     cabinet = forms.CharField(required=False)
#     host_cabinet_id = forms.CharField(required=False)
#     status = forms.CharField(required=False)
#     buy_date = forms.DateField(required=False)
#     admin = forms.CharField(required=False)
#     memo = forms.CharField(required=False)