#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
import json
from django.views import View
from django.http import JsonResponse
from django.urls import reverse as url_reverse
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required

from database import models
from backend.form import AssetForm
from backend.response import BaseResponse
from web.configure import assets


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
    def get(self, request):
        json_data_list = url_reverse('host_json_list')
        pagename = '主机管理'
        return render(request, 'default/public_list.html', locals())


class HostJsonList(View):
    """
    给ajax提供数据
    """
    def get(self, request):
        obj = assets.Host()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def post(self, request):
        response = assets.Host.delete_assets(request)
        return JsonResponse(response.__dict__)



class HostDetail(View):
    """
    主机详细信息
    """
    def get(self, request, host_id):
        status = models.Host.status_choices
        host_obj = get_object_or_404(models.Host, id=host_id)
        return render(request, 'assets/host_detail.html', locals())

    def post(self, request, host_id):
        status = models.Host.status_choices
        host_obj = get_object_or_404(models.Host, id=host_id)
        return render(request, 'assets/host_detail.html', locals())


class HostAdd(View):
    """
    添加主机
    """
    def get(self, request):
        json_data_list = url_reverse('host_add')
        device_types = models.Host.host_type_choices
        status = models.Host.status_choices
        raid_types = models.Host.raid_type_choices
        idcs = models.IDC.objects.all()
        manufactories = models.Manufactory.objects.all()
        return render(request, 'assets/host_add.html', locals())

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


class HostManagement(View):
    """
    修改主机
    """
    def get(self, request, host_id):
        json_data_list = '/assets/host_management/'
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

    def post(self, request, host_id):
        rep = BaseResponse()
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


class HostUpdate(View):
    """
    主动更新主机基础信息，暂未使用
    """
    def post(self, request):
        host_id = request.POST.get('id')
        return HttpResponse('host_update')


@login_required
def network_list(request):
    network_devices = models.NetDevice.objects.all()
    status = models.NetDevice.status_choices
    return render(request, 'default/index.html', locals())


@login_required
def network_add(request):
    status = models.NetDevice.status_choices
    idcs = models.IDC.objects.all()
    manufactorys = models.Manufactory.objects.all()
    return render(request, 'default/index.html', locals())


@login_required
def network_detail(request, network_id):
    status = models.NetDevice.status_choices
    if network_id:
        network_obj = models.NetDevice.objects.get(id=network_id)
    return render(request, 'default/index.html', locals())


@login_required
def network_update(request):
    return render(request, 'default/index.html')


@login_required
def network_del(request):
    return render(request, 'default/index.html')