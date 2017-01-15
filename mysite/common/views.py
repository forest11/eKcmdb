import json
from django.shortcuts import render, HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from assets import models
from backend.response import BaseResponse
from common import forms


@login_required
def business_list(request):
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
    if request.method == 'GET':
        services = models.Service.objects.all()
        return render(request, "common/business_add.html", locals())
    elif request.method == 'POST':
        rep = BaseResponse()
        print(request.POST)
        form = forms.BusinessForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                rep.status = True
            except Exception as e:
                rep.message = {'msg': [{'message': str(e)}]}
        else:
            error_dict = form.errors.as_json()
            rep.message = json.loads(error_dict)
        return HttpResponse(json.dumps(rep.__dict__))


@login_required
def service_list(request):
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
    if request.method == 'GET':
        hosts = models.Host.objects.all()
        return render(request, "common/service_add.html", locals())
    elif request.method == 'POST':
        rep = BaseResponse()
        form = forms.ServiceForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                rep.status = True
            except Exception as e:
                rep.message = {'msg': [{'message': str(e)}]}
        else:
            error_dict = form.errors.as_json()
            rep.message = json.loads(error_dict)
        return HttpResponse(json.dumps(rep.__dict__))

