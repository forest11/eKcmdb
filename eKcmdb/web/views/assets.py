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
from backend.form import AssetForm
from backend.auth.AccessAuth import check_auth
from backend.response import BaseResponse
from web.configure import assets


@login_required
def index(request):
    """
    仪表盘
    :param request:
    :return:
    """
    hosts = models.Host.objects.all().count()
    users = models.UserProfile.objects.all().count()
    return render(request, 'default/dashboard.html', locals())


class HostList(View):
    """
    主机列表页
    """
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        json_data_list = url_reverse('host_json_list')
        pagename = '主机管理'
        return render(request, 'default/public_list.html', locals())


class HostJsonList(View):
    """
    给ajax提供数据
    """
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        obj = assets.Host()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    @method_decorator(login_required)
    @method_decorator(check_auth)
    def post(self, request):
        response = assets.Host.delete_assets(request)
        return JsonResponse(response.__dict__)


class HostDetail(View):
    """
    主机详细信息
    """
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        status = models.Host.status_choices
        host_id = request.GET.get('id')
        host_obj = get_object_or_404(models.Host, id=host_id)
        return render(request, 'assets/host_detail.html', locals())


class HostAdd(View):
    """
    添加主机
    """
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        json_data_list = url_reverse('host_add')
        device_types = models.Host.host_type_choices
        status = models.Host.status_choices
        raid_types = models.Host.raid_type_choices
        idcs = models.IDC.objects.all()
        manufactories = models.Manufactory.objects.all()
        return render(request, 'assets/host_add.html', locals())

    @method_decorator(login_required)
    @method_decorator(check_auth)
    def post(self, request):
        rep = BaseResponse()
        form = AssetForm.HostForm(request.POST)
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


class HostUpdate(View):
    """
    修改主机
    """
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def get(self, request):
        json_data_list = url_reverse('host_update')
        host_id = request.GET.get('id')
        host_obj = get_object_or_404(models.Host, id=host_id)
        idcs = models.IDC.objects.all()
        business_units = models.BusinessUnit.objects.all()
        services = models.Service.objects.all()
        device_types = models.Host.host_type_choices
        raid_types = models.Host.raid_type_choices
        status = models.Host.status_choices
        os_types = models.System.objects.all()
        manufactories = models.Manufactory.objects.all()
        return render(request, 'assets/host_update.html', locals())

    @method_decorator(login_required)
    @method_decorator(check_auth)
    def post(self, request):
        rep = BaseResponse()
        host_id = request.GET.get('id')
        host_obj = get_object_or_404(models.Host, id=host_id)
        form = AssetForm.HostForm(request.POST, instance=host_obj)
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


class HostGrain(View):
    """
    主动更新主机基础信息，暂未使用
    """
    @method_decorator(login_required)
    @method_decorator(check_auth)
    def post(self, request):
        host_id = request.POST.get('id')
        return HttpResponse('host_update')

