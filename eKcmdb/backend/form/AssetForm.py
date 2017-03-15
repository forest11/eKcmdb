# -*- coding: utf-8 -*-
# __Author__: PanDongLin
from django.core.exceptions import ValidationError
from django import forms
from database import models


class HostForm(forms.ModelForm):
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

