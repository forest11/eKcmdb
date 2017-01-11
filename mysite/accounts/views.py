from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from accounts import forms, models
from backend.response import BaseResponse
from backend import CheckCode, EmailSend, RandomCode
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json
import io


def create_code(request):
    stream = io.BytesIO()
    img, code = CheckCode.create_validate_code()
    img.save(stream, 'png')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())


def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/assets/index/')
    if request.method == "POST":
        rep = BaseResponse()
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            rec_data = form.clean()
            user = authenticate(email=rec_data['email'], password=rec_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
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
    logout(request)
    return HttpResponseRedirect('/accounts/login/')


@login_required
def change_pwd(request):
    if request.method == 'POST':
        rep = BaseResponse()
        form = forms.ChangePwd(request.POST)
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
                else:
                    rep.message = {'new_password2': [{'message': '2次输入不一致'}]}
            else:
                rep.message = {'old_password': [{'message': '旧密码错误'}]}
        else:
            error_dict = form.errors.as_json()
            rep.message = json.loads(error_dict)
    return render(request, 'accounts/change_pwd.html', locals())


@login_required
def show_message(request):
    if request.method == 'POST':
        msg = request.POST.get("msg", "")
        msg_list = msg.split("-")
        #输入不为空，分割后为int类型数据，以及所有值不能大于user_key的长度
        if msg_list and all([i.isdigit() for i in msg_list]) and all([int(i)<len(request.user.user_key) for i in msg_list]):
            ret = [request.user.user_key[int(i)] for i in msg_list]
        else:
            ret = "输入错误"
        return HttpResponse(ret)
    return render(request, 'accounts/show_message.html')


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
                times = models.CheckCode.objects.filter(email=email, ctime__gt=limit_time, times__gt=3).count() #当前1小时内，是否超过3次
                if times:
                    rep.summary = "'已超最大次数（1小时后重试）'"
                else:
                    unfreeze = models.CheckCode.objects.filter(email=email, ctime__lt=limit_time).count()
                    if unfreeze:
                        models.CheckCode.objects.filter(email=email).update(times=0)
                    from django.db.models import F
                    models.CheckCode.objects.filter(email=email).update(code=code.lower(), ctime=current_date, times=F('times')+1)
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
    if request.method == 'POST':
        rep = BaseResponse()
        form = forms.CheckCode(request.POST)
        if form.is_valid():
            rec_data = form.clean()
            limit_time = timezone.now() - timezone.timedelta(minutes=1)  # 1分钟前的时间
            code_check = models.CheckCode.objects.filter(email=rec_data['email'],
                                                         code=rec_data['code'].lower(),   #用户输入，需要转成小写
                                                         ctime__gt=limit_time
                                                         ).count()  #判断用户输入的email和验证码是否和数据库中的一致,且在1分钟内
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
    forget_user = request.session.get('forget_user', None) #忘记密码用户通过验证，写到session中
    if forget_user:
        if request.method == 'POST':
            rep = BaseResponse()
            form = forms.ResetPwd(request.POST)
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


def response_404_handler(request):
    return render(request, 'common/404.html', status=404)
