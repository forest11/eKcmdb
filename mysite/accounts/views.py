import json
import io
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from backend.response import BaseResponse
from backend import CheckCode, EmailSend, RandomCode
from accounts import forms, models


def response_404_handler(request):
    """
    定义404错误
    :param request:
    :return:
    """
    return render(request, 'common/404.html', status=404)


def create_code(request):
    """
    生成随机吗
    :param request:
    :return:
    """
    stream = io.BytesIO()
    img, code = CheckCode.create_validate_code()
    img.save(stream, 'png')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())


def format_url(url_dict):
    """
    格式化url
    :param url_dict:
    :return:
    """
    key = "%s" % url_dict['perm__code']
    value = {"method": url_dict['perm__method'], 'kwargs': url_dict['perm__kwargs']}
    return key, value


def ret_url_method(perm_list):
    """
    权限列表格式化为字典类型
    :param perm_list:
    :return:
    """
    perm_dict = {}
    for item in perm_list:
        key, value = format_url(item)
        perm_dict[key] = value
    return perm_dict


def user_login(request):
    """
    用户登陆认证
    :param request:
    :return:
    """
    if request.method == "POST":
        rep = BaseResponse()
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            rec_data = form.clean()
            user = authenticate(email=rec_data['email'], password=rec_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    role_id_list = models.UserProfile.objects.filter(id=request.user.id).values('role')
                    perm_queryset = models.Role.objects.filter(id__in=role_id_list).values(
                        'perm__code',
                        'perm__method',
                        'perm__kwargs')
                    perm_dict = ret_url_method(list(perm_queryset))
                    perm_list = list(perm_dict.keys())
                    request.session['perm_list'] = perm_list
                    return HttpResponseRedirect('/assets/index/')
                else:
                    rep.message = {'email': [{'message': '账号被禁用'}]}
            else:
                rep.message = {'email': [{'message': '邮箱或密码错误'}]}
        else:
            error_dict = form.errors.as_json() #json格式的错误数据
            rep.message = json.loads(error_dict)
    return render(request, 'accounts/login.html', locals())


def user_logout(request):
    """用户退出"""
    logout(request)
    return HttpResponseRedirect('/accounts/login/')


@login_required
def change_pwd(request):
    """
    修改密码
    :param request:
    :return:
    """
    if request.method == 'POST':
        rep = BaseResponse()
        form = forms.ChangePwdForm(request.POST)
        if form.is_valid():
            rec_data = form.clean()
            old_password = rec_data['old_password']
            new_password1 = rec_data['new_password1']
            new_password2 = rec_data['new_password2']
            user = authenticate(email=request.user, password=old_password)
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
    return render(request, 'accounts/change_pwd.html', locals())


def send_msg(request):
    """
    生成对验证码，带大小写，数字，存到数据库中时，全部转成了小写
    :param request:
    :return:
    """
    rep = BaseResponse()
    form = forms.SendMsgForm(request.POST)
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
                print("当前注册码为:", code)  # 输出当前验证码
                EmailSend.email(email.split(), code)   #发送验证码到邮箱
                rep.status = True
            else:   #不是第1次发送
                limit_time = current_date - timezone.timedelta(hours=1)   #1小时前的时间
                times = models.CheckCode.objects.filter(email=email, ctime__gt=limit_time,
                                                        times__gt=3).count()  # 当前1小时内，是否超过3次
                if times:
                    rep.summary = "'已超最大次数（1小时后重试）'"
                else:
                    unfreeze = models.CheckCode.objects.filter(email=email, ctime__lt=limit_time).count()
                    if unfreeze:
                        models.CheckCode.objects.filter(email=email).update(times=0)
                    from django.db.models import F
                    models.CheckCode.objects.filter(email=email).update(code=code.lower(), ctime=current_date,
                                                                        times=F('times') + 1)
                    print("当前注册码为:", code)  # 输出当前验证码
                    EmailSend.email(email.split(), code)
                    rep.status = True
        else:
            rep.summary = '邮箱未注册'
            return HttpResponse(json.dumps(rep.__dict__))
    else:
        error_dict = json.loads(form.errors.as_json())
        rep.summary = error_dict['email'][0]['message']
    return HttpResponse(json.dumps(rep.__dict__))


def forget_pwd(request):
    """
    用户找回密码
    :param request:
    :return:
    """
    if request.method == 'POST':
        rep = BaseResponse()
        form = forms.CheckCode(request.POST)
        if form.is_valid():
            rec_data = form.clean()
            limit_time = timezone.now() - timezone.timedelta(minutes=1)  # 1分钟前的时间
            code_check = models.CheckCode.objects.filter(email=rec_data['email'],
                                                         code=rec_data['code'].lower(),   #用户输入，需要转成小写
                                                         ctime__gt=limit_time
                                                         ).count() #判断用户输入的email和验证码是否和数据库中的一致,且在1分钟内
            if code_check:
                request.session['forget_user'] = rec_data['email']
                return HttpResponseRedirect('/accounts/reset_pwd/')
            else:
                rep.message = {'code': [{'message': '验证码错误或失效'}]}
        else:
            error_dict = form.errors.as_json()
            rep.message = json.loads(error_dict)
        # return HttpResponse(json.dumps(rep.__dict__))
    return render(request, 'accounts/forget_pwd.html', locals())


def reset_pwd(request):
    """
    重设密码
    :param request:
    :return:
    """
    forget_user = request.session.get('forget_user', None) #忘记密码用户通过验证，写到session中
    if forget_user:
        if request.method == 'POST':
            rep = BaseResponse()
            form = forms.ResetPwdForm(request.POST)
            if form.is_valid():
                rec_data = form.clean()
                new_password1 = rec_data['new_password1']
                new_password2 = rec_data['new_password2']
                if new_password1 == new_password2:
                    user_obj = models.UserProfile.objects.get(email=forget_user)
                    user_obj.set_password(new_password2)
                    user_obj.save()
                    del request.session['forget_user']
                    rep.status = True
                else:
                    rep.message = {'resetpwd': [{'message': '2次输入不一致'}]}
            else:
                error_dict = form.errors.as_json()
                rep.message = json.loads(error_dict)
            return HttpResponse(json.dumps(rep.__dict__))
        return render(request, 'accounts/reset_pwd.html')
    else:
        return HttpResponseRedirect('/accounts/login/')


@login_required
def user_list(request):
    """
    用户列表
    :param request:
    :return:
    """
    if request.method == 'GET':
        user_obj = models.UserProfile.objects.all()
        paginator = Paginator(user_obj, 10)
        page = request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except (InvalidPage, PageNotAnInteger):
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "accounts/user_list.html", locals())


@login_required
def user_add(request):
    """
    添加用户
    :param request:
    :return:
    """
    roles = models.Role.objects.all()
    if request.method == 'POST':
        rep = BaseResponse()
        form = forms.UserForm(request.POST)
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
        return HttpResponse(json.dumps(rep.__dict__))
    return render(request, "accounts/user_add.html", locals())


@login_required
def user_del(request):
    """
    删除用户
    :param request:
    :return:
    """
    if request.method == 'POST':
        user_id = request.POST.get('id')
        del_user = models.UserProfile.objects.filter(id=user_id).delete()
        if del_user:
            return HttpResponse(204)
    return HttpResponse(500)


@login_required
def user_update(request, user_id):
    """修改用户"""
    user_obj = get_object_or_404(models.UserProfile, id=user_id)
    roles = models.Role.objects.all()
    if request.method == 'POST':
        rep = BaseResponse()
        form = forms.UpdateUserForm(request.POST, instance=user_obj)
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
        return HttpResponse(json.dumps(rep.__dict__))
    return render(request, "accounts/user_update.html", locals())


@login_required
def role_list(request):
    """
    角色列表
    :param request:
    :return:
    """
    role_obj = models.Role.objects.all()
    paginator = Paginator(role_obj, 10)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except (InvalidPage, PageNotAnInteger):
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, "accounts/role_list.html", locals())


@login_required
def role_add(request):
    """添加角色"""
    permissions = models.Permission.objects.all()
    if request.method == 'POST':
        rep = BaseResponse()
        form = forms.RoleForm(request.POST)
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
        return HttpResponse(json.dumps(rep.__dict__))
    return render(request, "accounts/role_add.html", locals())


@login_required
def role_update(request, role_id):
    """
    修改角色
    :param request:
    :param role_id:
    :return:
    """
    role_obj = get_object_or_404(models.Role, id=role_id)
    permissions = models.Permission.objects.all()
    if request.method == 'POST':
        rep = BaseResponse()
        form = forms.RoleForm(request.POST, instance=role_obj)
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
        return HttpResponse(json.dumps(rep.__dict__))
    return render(request, "accounts/role_update.html", locals())


@login_required
def role_del(request):
    """
    删除角色
    :param request:
    :return:
    """
    if request.method == 'POST':
        role_id = request.POST.get('id')
        del_role = models.Role.objects.filter(id=role_id).delete()
        if del_role:
            return HttpResponse(204)
    return HttpResponse(500)


@login_required
def permission_list(request):
    """权限列表"""
    permission_obj = models.Permission.objects.all()
    paginator = Paginator(permission_obj, 10)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except (InvalidPage, PageNotAnInteger):
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, "accounts/permission_list.html", locals())


@login_required
def permission_add(request):
    """
    添加权限
    :param request:
    :return:
    """
    if request.method == 'POST':
        rep = BaseResponse()
        form = forms.PermissionForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                rep.status = True
            except Exception as e:
                rep.message = {'msg-error': [{'message': str(e)}]}
        else:
            error_dict = form.errors.as_json()
            rep.message = json.loads(error_dict)
        return HttpResponse(json.dumps(rep.__dict__))
    return render(request, "accounts/permission_add.html")


@login_required
def permission_update(request, perm_id):
    """
    修改权限
    :param request:
    :param perm_id:
    :return:
    """
    if request.method == 'POST':
        rep = BaseResponse()
        try:
            perm_obj = models.Permission.objects.get(id=perm_id)
            form = forms.PermissionForm(request.POST, instance=perm_obj)
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
        return HttpResponse(json.dumps(rep.__dict__))


@login_required
def permission_del(request):
    """
    删除权限
    :param request:
    :return:
    """
    if request.method == 'POST':
        permission_id = request.POST.get('id')
        del_permission = models.Permission.objects.filter(id=permission_id).delete()
        if del_permission:
            return HttpResponse(204)
    return HttpResponse(500)
