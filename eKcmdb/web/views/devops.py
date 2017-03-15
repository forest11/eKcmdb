#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
import json
from django.views import View
from django.http import JsonResponse
from django.urls import reverse as url_reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, get_object_or_404

from database import models
from backend.form import DevopsForm
from backend.response import BaseResponse
from backend.devops import task_handle
from web.configure import devops


class BusinessList(View):
    """业务线列表"""

    def get(self, request):
        json_data_list = url_reverse('business_json_list')
        pagename = '业务线列表'
        return render(request, 'default/public_list.html', locals())


class BusinessJsonList(View):
    def get(self, request):
        obj = devops.Business()
        response = obj.fetch_business(request)
        return JsonResponse(response.__dict__)

    def post(self, request):
        response = devops.Business.delete_business(request)
        return JsonResponse(response.__dict__)


class BusinessAdd(View):
    """添加业务线"""

    def get(self, request):
        json_data_list = url_reverse('business_add')
        services = models.Service.objects.all()
        return render(request, "devops/business_add.html", locals())

    def post(self, request):
        rep = BaseResponse()
        form = DevopsForm.BusinessForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                form.save_m2m()
                rep.status = True
            except Exception as e:
                rep.message = {'msg': [{'message': str(e)}]}
        else:
            error_dict = form.errors.as_json()
            rep.message = json.loads(error_dict)
        return JsonResponse(rep.__dict__)


class BusinessManagement(View):
    """修改业务线"""

    def get(self, request, business_id):
        json_data_list = '/devops/business_management/'
        business_obj = get_object_or_404(models.BusinessUnit, id=business_id)
        services = models.Service.objects.all()
        return render(request, "devops/business_update.html", locals())

    def post(self, request, business_id):
        rep = BaseResponse()
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

    def get(self, request):
        json_data_list = url_reverse('server_json_list')
        pagename = '服务列表'
        return render(request, 'default/public_list.html', locals())


class ServiceJsonList(View):
    def get(self, request):
        obj = devops.Service()
        response = obj.fetch_services(request)
        return JsonResponse(response.__dict__)

    def post(self, request):
        response = devops.Service.delete_service(request)
        return JsonResponse(response.__dict__)


class ServiceAdd(View):
    """添加服务"""

    def get(self, request):
        json_data_list = url_reverse('service_add')
        hosts = models.Host.objects.all()
        return render(request, "devops/service_add.html", locals())

    def post(self, request):
        rep = BaseResponse()
        form = DevopsForm.ServiceForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                form.save_m2m()
                rep.status = True
            except Exception as e:
                rep.message = {'msg': [{'message': str(e)}]}
        else:
            error_dict = form.errors.as_json()
            rep.message = json.loads(error_dict)
        return JsonResponse(rep.__dict__)


class ServiceManagement(View):
    """修改服务"""

    def get(self, request, service_id):
        json_data_list = '/devops/service_management/'
        service_obj = get_object_or_404(models.Service, id=service_id)
        hosts = models.Host.objects.all()
        service_host = service_obj.host.all()
        return render(request, "devops/service_update.html", locals())

    def post(self, request, service_id):
        rep = BaseResponse()
        service_obj = get_object_or_404(models.Service, id=service_id)
        form = DevopsForm.ServiceForm(request.POST, instance=service_obj)
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


class CheckSql(View):
    """
     SQL语句检查
    """

    def get(self, request):
        return render(request, 'devops/sql_check.html')

    def post(self, request):
        rep = BaseResponse()
        content = request.POST.get('content')
        if content:
            from backend.devops import run_cmd
            result, status = run_cmd.ssh_host_exec_cmd(0, '192.168.10.199', 22, 'root', 'Python-147', 'which', content)
            rep.status = True
            rep.data = result.decode('utf8')
        return JsonResponse(rep.__dict__)


class ShowMessage(View):
    """
    用于跳板机登陆认证，暂未使用
    """

    def get(self, request):
        return render(request, 'devops/show_message.html')

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
    def get(self, request):
        return render(request, 'devops/multi_cmd.html')


def task_center(request):
    if request.method == "POST":
        task_obj = task_handle.TaskHander(request)
        if task_obj.is_valid():
            task_obj.start()
            response = {'task_id': task_obj.task.id}
        else:
            response = {'errors': task_obj.errors}
        return HttpResponse(json.dumps(response))


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
    def get(self, request):
        return render(request, 'devops/code_ops.html')


class CodeLog(View):
    def get(self, request):
        return render(request, 'default/timeline.html')
