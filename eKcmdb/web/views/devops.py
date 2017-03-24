#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
import json
from django.views import View
from django.http import JsonResponse
from django.urls import reverse as url_reverse
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from database import models
from backend.form import DevopsForm
from backend.auth.AccessAuth import check_auth
from backend.response import BaseResponse
from backend.devops import task_handle
from backend.sqlcheck import inception
from web.configure import devops
from pagination.pager import PageInfo


class BusinessList(View):
    """业务线列表"""
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        pagename = '业务线列表'
        sql_ret = models.BusinessUnit.objects.all()
        bus_list = list(sql_ret)
        return render(request, 'devops/jsTree.html', locals())


class BusinessAdd(View):
    """添加业务线"""
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        json_data_list = url_reverse('business_add')
        services = models.Service.objects.all()
        return render(request, "devops/business_add.html", locals())

    @method_decorator(login_required)
    @method_decorator(check_auth)
    def post(self, request):
        rep = BaseResponse()
        form = DevopsForm.BusinessForm(request.POST)
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


class BusinessUpdate(View):
    """修改业务线"""
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        json_data_list = url_reverse('business_update')
        business_id = request.GET.get('id')
        business_obj = get_object_or_404(models.BusinessUnit, id=business_id)
        services = models.Service.objects.all()
        return render(request, "devops/business_update.html", locals())

    @method_decorator(login_required)
    @method_decorator(check_auth)
    def post(self, request):
        rep = BaseResponse()
        business_id = request.GET.get('id')
        business_obj = get_object_or_404(models.BusinessUnit, id=business_id)
        form = DevopsForm.BusinessForm(request.POST, instance=business_obj)
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


class ServiceList(View):
    """服务列表"""
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        json_data_list = url_reverse('server_json_list')
        pagename = '服务列表'
        return render(request, 'default/public_list.html', locals())


class ServiceJsonList(View):
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        obj = devops.Service()
        response = obj.fetch_services(request)
        return JsonResponse(response.__dict__)

    @method_decorator(login_required)
    @method_decorator(check_auth)
    def post(self, request):
        response = devops.Service.delete_service(request)
        return JsonResponse(response.__dict__)


class ServiceAdd(View):
    """添加服务"""
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        json_data_list = url_reverse('service_add')
        hosts = models.Host.objects.all()
        return render(request, "devops/service_add.html", locals())

    @method_decorator(login_required)
    @method_decorator(check_auth)
    def post(self, request):
        rep = BaseResponse()
        form = DevopsForm.ServiceForm(request.POST)
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


class ServiceUpdate(View):
    """修改服务"""
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        json_data_list = url_reverse('service_update')
        service_id = request.GET.get('id')
        service_obj = get_object_or_404(models.Service, id=service_id)
        hosts = models.Host.objects.all()
        service_host = service_obj.host.all()
        return render(request, "devops/service_update.html", locals())

    @method_decorator(login_required)
    @method_decorator(check_auth)
    def post(self, request):
        rep = BaseResponse()
        service_id = request.GET.get('id')
        service_obj = get_object_or_404(models.Service, id=service_id)
        form = DevopsForm.ServiceForm(request.POST, instance=service_obj)
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


class CheckSql(View):
    """
     SQL语句检查
    """
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        return render(request, 'devops/sql_check.html')

    @method_decorator(login_required)
    @method_decorator(check_auth)
    def post(self, request):
        rep = BaseResponse()
        form = DevopsForm.SQLCheck(request.POST)
        if form.is_valid():
            try:
                error_list = ['sql1', 'sq2']
                # inception_obj = inception.Inception()
                # sql_result = inception_obj.sqlauto_review(form.cleaned_data['sql_content'])
                # for row in sql_result:
                #     if row[1] == 1 or row[2] == 2:
                #         #状态1为警告，2表示严重错误，必须修改
                #         error_list.append(row[4])
                sql_obj = models.SqlCheck(
                    name=form.cleaned_data['name'],
                    pusher=request.user,
                    sql_content=form.cleaned_data['sql_content'],
                    sql_result=json.dumps(error_list),
                )
                sql_obj.save()
                rep.data = error_list
                rep.status = True
            except Exception as e:
                rep.message = {'msg-error': [{'message': str(e)}]}
        else:
            error_dict = form.errors.as_json()
            rep.message = json.loads(error_dict)
        return JsonResponse(rep.__dict__)


class SqlLog(View):
    """
    sql执行记录
    """
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        logs_count = models.SqlCheck.objects.all().count()
        page_info = PageInfo(request.GET.get('pager', None), logs_count)
        logs = models.SqlCheck.objects.all().order_by('-exec_time')[page_info.start:page_info.end]
        return render(request, 'devops/sql_log.html', locals())


class ShowMessage(View):
    """
    用于跳板机登陆认证，暂未使用
    """
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        return render(request, 'devops/show_message.html')

    @method_decorator(login_required)
    @method_decorator(check_auth)
    def post(self, request):
        rep = BaseResponse()
        msg = request.POST.get("msg", "")
        msg_list = msg.split("-")
        # 输入不为空，分割后为int类型数据，以及所有值不能大于user_key的长度
        if msg_list and all([i.isdigit() for i in msg_list]) and all(
                [int(i) < len(request.user.user_key) for i in msg_list]):
            rep.status = True
            rep.data = "".join([request.user.user_key[int(i)] for i in msg_list])
        return JsonResponse(rep.__dict__)


class MuliCmd(View):
    """
    批量执行
    """
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        return render(request, 'devops/multi_cmd.html')


@login_required
@check_auth
def task_center(request):
    if request.method == "POST":
        task_obj = task_handle.TaskHander(request)
        if task_obj.is_valid():
            task_obj.start()
            response = {'task_id': task_obj.task.id}
        else:
            response = {'errors': task_obj.errors}
        return HttpResponse(json.dumps(response))


@login_required
@check_auth
def get_task_result(request):
    task_id = request.GET.get('task_id')
    task_result = models.TaskDetail.objects.filter(bing_task_id=task_id).values('id',
                                                                                'exec_status',
                                                                                'event_log',
                                                                                'bind_host__host__hostname',
                                                                                'bind_host__remote_user__username')
    task_result_list = list(task_result)
    # return HttpResponse(json.dumps(task_result, default=json_date_handler))
    return HttpResponse(json.dumps(task_result_list))


class CodeOps(View):
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        return render(request, 'devops/code_ops.html')


class CodeLog(View):
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        return render(request, 'default/timeline.html')
