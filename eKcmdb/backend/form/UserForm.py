#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin

import re
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from database import models


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='用户密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = models.UserProfile
        fields = ('email', 'name')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("2次输入不相同")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.UserProfile
        exclude = ()
        # fields = ('email', 'name', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial['password']


def mobile_validate(value):
    """
    验证手机号码
    :param value:
    :return:
    """
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')


def tel_validate(value):
    """
    验证座机号码
    :param value:
    :return:
    """
    tel_re = re.compile(r'^((0\d{2,3})-)(\d{7,8})(-(\d{3,}))?$')
    if not tel_re.match(value):
        raise ValidationError('座机号码格式错误')


class LoginForm(forms.Form):
    """
    登陆验证
    """
    name = forms.CharField(max_length=32, error_messages={'required': '用户名不能为空', 'max_length': '密码最多32位'})
    password = forms.CharField(min_length=6, max_length=18, error_messages={'required': '密码不能为空',
                                                                            'min_length': '密码至少6位',
                                                                            'max_length': '密码最多18位'})


class ChangePwdForm(forms.Form):
    """
    修改密码验证
    """
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
    """
    生成验证码，需要对用户验证
    """
    email = forms.EmailField(error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'})


class CheckCode(forms.Form):
    """
    发送信息验证，此为找回密码时使用的form
    """
    email = forms.EmailField(error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'})
    code = forms.CharField(error_messages={'required': '验证码不能为空', 'invalid': '验证码错误'})


class ResetPwdForm(forms.Form):
    """
    重设密码验证
    """
    new_password1 = forms.CharField(min_length=6, max_length=18, error_messages={'required': '密码不能为空',
                                                                                 'min_length': '密码至少6位',
                                                                                 'max_length': '密码最多18位'})
    new_password2 = forms.CharField(min_length=6, max_length=18, error_messages={'required': '密码不能为空',
                                                                                 'min_length': '密码至少6位',
                                                                                 'max_length': '密码最多18位'})


class UserForm(forms.ModelForm):
    """
    添加用户form
    """
    class Meta:
        model = models.UserProfile
        fields = ('name', 'email', 'password', 'mobile', 'tel', 'department', 'role')

    def clean(self):
        cleaned_data = super(UserForm, self).clean() # 拿到所有表单的值
        name = self.cleaned_data.get("name")
        try:
            models.UserProfile.objects.get(name=name)
            self._errors["name"] = self.error_class(["用户%s已存在" % name])
        except:
            pass
        return cleaned_data

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UpdateUserForm(forms.ModelForm):
    """
    更新用户信息form
    """
    class Meta:
        model = models.UserProfile
        fields = ('name', 'email', 'is_active', 'mobile', 'tel', 'department', 'role')

    def save(self, commit=True):
        user = super(UpdateUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class RoleForm(forms.ModelForm):
    """角色"""
    class Meta:
        model = models.Role
        exclude = ("id", )

    def save(self, commit=True):
        role = super(RoleForm, self).save(commit=False)
        if commit:
            role.save()
        return role


class PermissionForm(forms.ModelForm):
    """
    权限
    """
    class Meta:
        model = models.Permission
        exclude = ("id",)

    def save(self, commit=True):
        perm = super(PermissionForm, self).save(commit=False)
        if commit:
            perm.save()
        return perm
