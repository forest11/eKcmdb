import json
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from assets import models
from backend.response import BaseResponse
from common import forms


@login_required
def business_list(request):
    """业务线列表"""
    business_obj = models.BusinessUnit.objects.all()
    paginator = Paginator(business_obj, 10)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except (InvalidPage, PageNotAnInteger):
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, "common/business_list.html", locals())


@login_required
def business_add(request):
    """添加业务线"""
    services = models.Service.objects.all()
    if request.method == 'POST':
        rep = BaseResponse()
        form = forms.BusinessForm(request.POST)
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
        return HttpResponse(json.dumps(rep.__dict__))
    return render(request, "common/business_add.html", locals())


@login_required
def business_del(request):
    """删除业务线"""
    if request.method == 'POST':
        business_id = request.POST.get('id')
        del_business = models.BusinessUnit.objects.filter(id=business_id).delete()
        if del_business:
            return HttpResponse(204)
    return HttpResponse(500)


@login_required
def business_update(request, business_id):
    """修改业务线"""
    business_obj = get_object_or_404(models.BusinessUnit, id=business_id)
    print('-----', business_obj.service.all())
    services = models.Service.objects.all()
    if request.method == 'POST':
        rep = BaseResponse()
        form = forms.BusinessForm(request.POST, instance=business_obj)
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
    return render(request, "common/business_update.html", locals())


@login_required
def service_list(request):
    """服务列表"""
    service_obj = models.Service.objects.all()
    paginator = Paginator(service_obj, 10)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except (InvalidPage, PageNotAnInteger):
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, "common/service_list.html", locals())


@login_required
def service_add(request):
    """添加服务"""
    hosts = models.Host.objects.all()
    if request.method == 'POST':
        rep = BaseResponse()
        form = forms.ServiceForm(request.POST)
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
        return HttpResponse(json.dumps(rep.__dict__))
    return render(request, "common/service_add.html", locals())


@login_required
def service_del(request):
    """删除服务"""
    if request.method == 'POST':
        service_id = request.POST.get('id')
        del_service = models.Service.objects.filter(id=service_id).delete()
        if del_service:
            return HttpResponse(204)
    return HttpResponse(500)


@login_required
def service_update(request, service_id):
    """修改服务"""
    service_obj = get_object_or_404(models.Service, id=service_id)
    hosts = models.Host.objects.all()
    service_host = service_obj.host.all()
    if request.method == 'POST':
        rep = BaseResponse()
        form = forms.ServiceForm(request.POST, instance=service_obj)
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
    return render(request, "common/service_update.html", locals())
