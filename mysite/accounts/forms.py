# -*- coding: utf-8 -*-
# __Author__: PanDongLin
from django import forms
from django.core.exceptions import ValidationError
import re


def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')


def tel_validate(value):
    tel_re = re.compile(r'^((0\d{2,3})-)(\d{7,8})(-(\d{3,}))?$')
    if not tel_re.match(value):
        raise ValidationError('座机号码格式错误')


class LoginForm(forms.Form):
    email = forms.EmailField(error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'})
    password = forms.CharField(min_length=6, max_length=18, error_messages={'required': '密码不能为空',
                                                                            'min_length': '密码至少6位',
                                                                            'max_length': '密码最多18位'})


class ChangePwdForm(forms.Form):
    old_password = forms.CharField(min_length=6, max_length=18, error_messages={'required': '密码不能为空',
                                                                                'min_length': '密码至少6位',
                                                                                'max_length': '密码最多18位'})
    new_password1 = forms.CharField(min_length=6, max_length=18, error_messages={'required': '密码不能为空',
                                                                                 'min_length': '密码至少6位',
                                                                                 'max_length': '密码最多18位'})
    new_password2 = forms.CharField(min_length=6, max_length=18, error_messages={'required': '密码不能为空',
                                                                                 'min_length': '密码至少6位',
                                                                                 'max_length': '密码最多18位'})


class SendMsgForm(forms.Form):
    email = forms.EmailField(error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'})


class CheckCode(forms.Form):
    email = forms.EmailField(error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'})
    code = forms.CharField(error_messages={'required': '验证码不能为空', 'invalid': '验证码错误'})


class ResetPwdForm(forms.Form):
    new_password1 = forms.CharField(min_length=6, max_length=18, error_messages={'required': '密码不能为空',
                                                                                 'min_length': '密码至少6位',
                                                                                 'max_length': '密码最多18位'})
    new_password2 = forms.CharField(min_length=6, max_length=18, error_messages={'required': '密码不能为空',
                                                                                 'min_length': '密码至少6位',
                                                                                 'max_length': '密码最多18位'})


class AddOrUpdateUserForm(forms.Form):
    email = forms.EmailField(error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'})
    name = forms.CharField(max_length=32, error_messages={'required': '用户名不能为空'})
    password = forms.CharField(required=False, min_length=6, max_length=18, error_messages={'min_length': '密码至少6位',
                                                                            'max_length': '密码最多18位'})
    is_active = forms.BooleanField(required=False)
    role = forms.CharField(required=False)
    mobile = forms.CharField(validators=[mobile_validate, ],)
    tel = forms.CharField(required=False, validators=[tel_validate, ],)

