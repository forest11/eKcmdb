#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin

from django import forms
from assets import models


class BusinessForm(forms.ModelForm):
    class Meta:
        model = models.BusinessUnit
        exclude = ("id",)

    def clean_service(self):
        service = self.cleaned_data.get('service')
        if not service:
            service = None
        return service


class ServiceForm(forms.ModelForm):
    class Meta:
        model = models.Service
        exclude = ("id",)

    def clean_host(self):
        host = self.cleaned_data.get('host')
        if not host:
            host = None
        return host