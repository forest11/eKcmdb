# -*- coding: utf-8 -*-
# __Author__: PanDongLin
from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'})
    password = forms.CharField(required=True, min_length=6, max_length=18, error_messages={'required': '密码不能为空',
                                                                                           'min_length': '密码至少6位',
                                                                                           'max_length': '密码最多18位'})


class ChangePwd(forms.Form):
    old_password = forms.CharField(required=True, min_length=6, max_length=18, error_messages={'required': '密码不能为空',
                                                                                               'min_length': '密码至少6位',
                                                                                               'max_length': '密码最多18位'})
    new_password1 = forms.CharField(required=True, min_length=6, max_length=18, error_messages={'required': '密码不能为空',
                                                                                                'min_length': '密码至少6位',
                                                                                                'max_length': '密码最多18位'})
    new_password2 = forms.CharField(required=True, min_length=6, max_length=18, error_messages={'required': '密码不能为空',
                                                                                                'min_length': '密码至少6位',
                                                                                                'max_length': '密码最多18位'})


class SendMsgForm(forms.Form):
    email = forms.EmailField(required=True, error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'})


class CheckCode(forms.Form):
    email = forms.EmailField(required=True, error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'})
    code = forms.CharField(required=True, error_messages={'required': '验证码不能为空', 'invalid': '验证码错误'})


class ResetPwd(forms.Form):
    new_password1 = forms.CharField(required=True, min_length=6, max_length=18, error_messages={'required': '密码不能为空',
                                                                                                'min_length': '密码至少6位',
                                                                                                'max_length': '密码最多18位'})
    new_password2 = forms.CharField(required=True, min_length=6, max_length=18, error_messages={'required': '密码不能为空',
                                                                                                'min_length': '密码至少6位',
                                                                                                'max_length': '密码最多18位'})
