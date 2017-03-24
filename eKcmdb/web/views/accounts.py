#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
import io
import json
from django.views import View
from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse as url_reverse
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from backend.response import BaseResponse
from backend.utils import CheckCode, FormatUrl, EmailSend, RandomCode
from backend.form import UserForm
from backend.auth.AccessAuth import check_auth
from web.configure import accounts
from database import models


def response_404_handler(request):
    """
    定义404错误
    :param request:
    :return:
    """
    return render(request, 'default/404.html', status=404)


def create_code(request):
    """
    生成随机码,暂未使用
    :param request:
    :return:
    """
    stream = io.BytesIO()
    img, code = CheckCode.create_validate_code()
    img.save(stream, 'png')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())


class LoginView(View):
    """
    用户登陆认证
    """
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        rep = BaseResponse()
        form = UserForm.LoginForm(request.POST)
        if form.is_valid():
            rec_data = form.clean()
            user = authenticate(name=rec_data['name'], password=rec_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    role_id_list = models.UserProfile.objects.filter(id=request.user.id).values('role')
                    perm_queryset = models.Role.objects.filter(id__in=role_id_list).values(
                        'perm__code',
                        'perm__method',
                        'perm__kwargs')
                    perm_dict = FormatUrl.ret_url_method(list(perm_queryset))
                    perm_list = list(perm_dict.keys())
                    request.session['perm_list'] = perm_list
                    rep.status = True
                    return JsonResponse(rep.__dict__)
                else:
                    rep.message = {'name': [{'message': '账号被禁用'}]}
            else:
                rep.message = {'name': [{'message': '邮箱或密码错误'}]}
        else:
            error_dict = form.errors.as_json() #json格式的错误数据
            rep.message = json.loads(error_dict)
        return JsonResponse(rep.__dict__)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(url_reverse('login'))


class ChangePassWd(View):
    """
    用户修改密码
    """
    def get(self, request):
        return render(request, 'accounts/change_pwd.html')

    def post(self, request):
        rep = BaseResponse()
        form = UserForm.ChangePwdForm(request.POST)
        if form.is_valid():
            rec_data = form.clean()
            old_password = rec_data['old_password']
            new_password1 = rec_data['new_password1']
            new_password2 = rec_data['new_password2']
            user = authenticate(name=request.user, password=old_password)
            if user is not None:
                if new_password1 == new_password2:
                    user.set_password(new_password2)
                    user.save()
                    rep.status = True
                else:
                    rep.message = {'new_password2': [{'message': '2次输入不一致'}]}
            else:
                rep.message = {'old_password': [{'message': '旧密码错误'}]}
        else:
            error_dict = form.errors.as_json()
            rep.message = json.loads(error_dict)
        return JsonResponse(rep.__dict__)


class SendMsg(View):
    """
    生成对验证码，带大小写，数字，存到数据库中时，全部转成了小写
    """
    def post(self, request):
        rep = BaseResponse()
        form = UserForm.SendMsgForm(request.POST)
        if form.is_valid():
            rec_data = form.clean()
            email = rec_data['email']
            has_exists_email = models.UserProfile.objects.filter(email=email).count()
            if has_exists_email:   #邮箱存在，则向邮箱发送6位数的随机字符串
                # current_date = datetime.datetime.now()
                current_date = timezone.now()
                code = RandomCode.random_code(6)
                counts = models.CheckCode.objects.filter(email=email).count()  #判断邮箱是否存在
                if not counts:   #向此邮箱第1次发送
                    models.CheckCode.objects.create(email=email, code=code.lower(), ctime=current_date)
                    print("当前code为:", code)  # 输出当前验证码
                    EmailSend.send_mail(email.split(), code, "密码找回")   #发送验证码到邮箱
                    rep.status = True
                else:   #不是第1次发送
                    limit_time = current_date - timezone.timedelta(hours=1)   #1小时前的时间
                    times = models.CheckCode.objects.filter(email=email, ctime__gt=limit_time,
                                                            times__gt=3).count()  # 当前1小时内，是否超过3次
                    if times:
                        rep.message = "'已超最大次数（1小时后重试）'"
                    else:
                        unfreeze = models.CheckCode.objects.filter(email=email, ctime__lt=limit_time).count()
                        if unfreeze:
                            models.CheckCode.objects.filter(email=email).update(times=0)
                        from django.db.models import F
                        models.CheckCode.objects.filter(email=email).update(code=code.lower(), ctime=current_date,
                                                                            times=F('times') + 1)
                        print("当前code为:", code)  # 输出当前验证码
                        EmailSend.send_mail(email.split(), code, "密码找回")
                        rep.status = True
            else:
                rep.message = '邮箱未注册'
                return JsonResponse(rep.__dict__)
        else:
            error_dict = json.loads(form.errors.as_json())
            rep.message = error_dict['email'][0]['message']
        return JsonResponse(rep.__dict__)


class ForgetPassWd(View):
    """
    用户找回密码
    """
    def get(self, request):
        return render(request, 'accounts/forget_pwd.html')

    def post(self, request):
        rep = BaseResponse()
        form = UserForm.CheckCode(request.POST)

        if form.is_valid():
            rec_data = form.clean()
            limit_time = timezone.now() - timezone.timedelta(minutes=5)  # 1分钟前的时间
            code_check = models.CheckCode.objects.filter(email=rec_data['email'],
                                                         code=rec_data['code'].lower(),   #用户输入，需要转成小写
                                                         ctime__gt=limit_time
                                                         ).count() #判断用户输入的email和验证码是否和数据库中的一致,且在1分钟内
            if code_check:
                request.session['forget_user'] = rec_data['email']
                rep.status = True
            else:
                rep.message = {'code': [{'message': 'email错误或验证码错误'}]}
        else:
            error_dict = form.errors.as_json()
            rep.message = json.loads(error_dict)
        return JsonResponse(rep.__dict__)


class RestPassWd(View):
    """
    用户重设密码
    """
    def get(self, request):
        return render(request, 'accounts/reset_pwd.html')

    def post(self, request):
        forget_user = request.session.get('forget_user', None) #需要重设密码并且通过验证用户通已写到session中
        if forget_user:
            rep = BaseResponse()
            form = UserForm.ResetPwdForm(request.POST)
            if form.is_valid():
                rec_data = form.clean()
                new_password1 = rec_data['new_password1']
                new_password2 = rec_data['new_password2']
                if new_password1 == new_password2:
                    user_obj = models.UserProfile.objects.get(email=forget_user)
                    user_obj.set_password(new_password2)
                    user_obj.save()
                    del request.session['forget_user']   #修改密码后删除session绘画
                    rep.status = True
                else:
                    rep.message = {'resetpwd': [{'message': '2次输入不一致'}]}
            else:
                error_dict = form.errors.as_json()
                rep.message = json.loads(error_dict)
            return JsonResponse(rep.__dict__)
        else:
            return HttpResponseRedirect(url_reverse('login'))


class UserList(View):
    """
    用户列表页
    """
    @method_decorator(login_required)
    def get(self, request):
        json_data_list = url_reverse('user_json_list')
        pagename = '用户列表'
        return render(request, 'default/public_list.html', locals())


class UserJsonList(View):
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        obj = accounts.User()
        response = obj.fetch_users(request)
        return JsonResponse(response.__dict__)

    @method_decorator(login_required)
    @method_decorator(check_auth)
    def post(self, request):
        response = accounts.User.delete_user(request)
        return JsonResponse(response.__dict__)


class UserAdd(View):
    """
    添加用户
    """
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        json_data_list = url_reverse('user_add')
        roles = models.Role.objects.all()
        departments = models.UserProfile.department_choices
        return render(request, "accounts/user_add.html", locals())

    @method_decorator(login_required)
    @method_decorator(check_auth)
    def post(self, request):
        rep = BaseResponse()
        form = UserForm.UserForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                form.save_m2m()
                rep.status = True
            except Exception as e:
                rep.message = {'msg-error': [{'message': str(e)}]}
        else:
            error_dict = form.errors.as_json()
            rep.message = json.loads(error_dict)
        return JsonResponse(rep.__dict__)


class UserUpdate(View):
    """用户管理"""
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        user_id = request.GET.get('id')
        json_data_list = url_reverse('user_update')
        user_obj = get_object_or_404(models.UserProfile, id=user_id)
        roles = models.Role.objects.all()
        departments = models.UserProfile.department_choices
        return render(request, "accounts/user_update.html", locals())

    @method_decorator(login_required)
    @method_decorator(check_auth)
    def post(self, request):
        rep = BaseResponse()
        user_id = request.GET.get('id')
        user_obj = get_object_or_404(models.UserProfile, id=user_id)
        form = UserForm.UpdateUserForm(request.POST, instance=user_obj)
        if form.is_valid():
            try:
                form.save()
                form.save_m2m()
                rep.status = True
            except Exception as e:
                rep.message = {'msg-error': [{'message': str(e)}]}
        else:
            error_dict = form.errors.as_json()
            rep.message = json.loads(error_dict)
        return JsonResponse(rep.__dict__)


class RoleList(View):
    """
    角色列表
    """
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        json_data_list = url_reverse('role_json_list')
        pagename = '角色列表'
        return render(request, 'default/public_list.html', locals())


class RoleJsonList(View):
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        obj = accounts.Role()
        response = obj.fetch_roles(request)
        return JsonResponse(response.__dict__)

    @method_decorator(login_required)
    @method_decorator(check_auth)
    def post(self, request):
        response = accounts.Role.delete_role(request)
        return JsonResponse(response.__dict__)


class RoleAdd(View):
    """
    添加角色
    """
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        json_data_list = url_reverse('role_add')
        permissions = models.Permission.objects.all()
        return render(request, "accounts/role_add.html", locals())

    @method_decorator(login_required)
    @method_decorator(check_auth)
    def post(self, request):
        rep = BaseResponse()
        form = UserForm.RoleForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                form.save_m2m()
                rep.status = True
            except Exception as e:
                rep.message = {'msg-error': [{'message': str(e)}]}
        else:
            error_dict = form.errors.as_json()
            rep.message = json.loads(error_dict)
        return JsonResponse(rep.__dict__)


class RoleUpdate(View):
    """修改角色"""
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        role_id = request.GET.get('id')
        role_obj = get_object_or_404(models.Role, id=role_id)
        json_data_list = url_reverse('role_update')
        permissions = models.Permission.objects.all()
        return render(request, "accounts/role_update.html", locals())

    @method_decorator(login_required)
    @method_decorator(check_auth)
    def post(self, request):
        role_id = request.GET.get('id')
        rep = BaseResponse()
        role_obj = get_object_or_404(models.Role, id=role_id)
        form = UserForm.RoleForm(request.POST, instance=role_obj)
        if form.is_valid():
            try:
                form.save()
                form.save_m2m()
                rep.status = True
            except Exception as e:
                rep.message = {'msg-error': [{'message': str(e)}]}
        else:
            error_dict = form.errors.as_json()
            rep.message = json.loads(error_dict)
        return JsonResponse(rep.__dict__)


class PermList(View):
    """
    权限列表
    """
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        json_data_list = url_reverse('permission_json_list')
        pagename = '权限列表'
        return render(request, 'default/public_list.html', locals())


class PermJsonList(View):
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        obj = accounts.Permission()
        response = obj.fetch_perms(request)
        return JsonResponse(response.__dict__)

    @method_decorator(login_required)
    @method_decorator(check_auth)
    def post(self, request):
        response = accounts.Permission.delete_perm(request)
        return JsonResponse(response.__dict__)


class PermAdd(View):
    """
    添加权限
    """
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        json_data_list = url_reverse('permission_add')
        return render(request, "accounts/permission_add.html", locals())

    @method_decorator(login_required)
    @method_decorator(check_auth)
    def post(self, request):
        rep = BaseResponse()
        form = UserForm.PermissionForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                rep.status = True
            except Exception as e:
                rep.message = {'msg-error': [{'message': str(e)}]}
        else:
            error_dict = form.errors.as_json()
            rep.message = json.loads(error_dict)
        return JsonResponse(rep.__dict__)


class PermUpdate(View):
    """
    更新权限
    """
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def post(self, request):
        perm_id = request.GET.get('id')
        rep = BaseResponse()
        try:
            perm_obj = models.Permission.objects.get(id=perm_id)
            form = UserForm.PermissionForm(request.POST, instance=perm_obj)
            if form.is_valid():
                rec_data = form.clean()
                try:
                    form.save()
                    #在当前页面通过ajax修改数据，需要把修改后的数据返回给前端
                    rep.data = {
                        "caption": rec_data["caption"],
                        "code":  rec_data["code"],
                        "method":  rec_data["method"],
                        "kwargs":  rec_data["kwargs"]
                    }
                    rep.status = True
                except Exception as e:
                    rep.message = {'msg-error': [{'message': str(e)}]}
            else:
                error_dict = form.errors.as_json()
                rep.message = json.loads(error_dict)
        except Exception as e:
            rep.message = {'msg-error': [{'message': str(e)}]}
        return JsonResponse(rep.__dict__)