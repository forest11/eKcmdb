import json
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from assets import models
from backend.response import BaseResponse
from common import forms


@login_required
def business_list(request):
    if request.method == 'GET':
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
    elif request.method == 'POST':
        rep = BaseResponse()
        form = forms.UpdateBusinessForm(request.POST)
        if form.is_valid():
            rec_data = form.clean()
            service = [ x for x in rec_data["service"].split("-") if x]
            try:
                business_obj = models.BusinessUnit.objects.get(id=rec_data["id"])
                old_service = business_obj.service.all().values_list("name", "port")
                for item in service:
                    name, port = item.split(":")
                    if (name, port) not in old_service:   #业务线新添加服务
                        business_obj.service.add(models.Service.objects.get(name=name, port=port))
                for item in old_service:
                    if "%s:%s" % (item[0], item[1]) not in service:  #业务线删除服务
                        business_obj.service.remove(models.Service.objects.get(name=item[0], port=item[1]))
                business_obj.memo = rec_data["memo"]
                business_obj.save()
                rep.status = True
                rep.summary = {
                    "service": service,
                    "memo": rec_data["memo"]
                }
            except Exception as e:
                rep.message = {'msg': [{'message': str(e)}]}
        else:
            error_dict = form.errors.as_json()
            rep.message = json.loads(error_dict)
        return HttpResponse(json.dumps(rep.__dict__))


@login_required
def business_add(request):
    if request.method == 'GET':
        services = models.Service.objects.all()
        return render(request, "common/business_add.html", locals())
    elif request.method == 'POST':
        rep = BaseResponse()
        form = forms.BusinessForm(request.POST)
        if form.is_valid():
            try:
                # form.save()
                rep.status = True
            except Exception as e:
                rep.message = {'msg': [{'message': str(e)}]}
        else:
            error_dict = form.errors.as_json()
            rep.message = json.loads(error_dict)
        return HttpResponse(json.dumps(rep.__dict__))


@login_required
def business_del(request):
    if request.method == 'POST':
        business_id = request.POST.get('id')
        del_business = models.BusinessUnit.objects.filter(id=business_id).delete()
        if del_business:
            return HttpResponse(204)
    return HttpResponse(500)


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


@login_required
def service_del(request):
    if request.method == 'POST':
        service_id = request.POST.get('id')
        del_service = models.Service.objects.filter(id=service_id).delete()
        if del_service:
            return HttpResponse(204)
    return HttpResponse(500)


@login_required
def service_update(request, id):
    if request.method == 'GET':
        hosts = models.Host.objects.all()
        service_obj = get_object_or_404(models.Service, id=id)
        service_host = service_obj.host.all()
        return render(request, "common/service_update.html", locals())
    elif request.method == 'POST':
        rep = BaseResponse()
        form = forms.UpdateServiceForm(request.POST)
        if form.is_valid():
            rec_data = form.clean()
            service = [x for x in rec_data["service"].split("-") if x]
            try:
                business_obj = models.BusinessUnit.objects.get(id=rec_data["id"])
                old_service = business_obj.service.all().values_list("name", "port")
                for item in service:
                    name, port = item.split(":")
                    if (name, port) not in old_service:  # 业务线新添加服务
                        business_obj.service.add(models.Service.objects.get(name=name, port=port))
                for item in old_service:
                    if "%s:%s" % (item[0], item[1]) not in service:  # 业务线删除服务
                        business_obj.service.remove(models.Service.objects.get(name=item[0], port=item[1]))
                business_obj.memo = rec_data["memo"]
                business_obj.save()
                rep.status = True
                rep.summary = {
                    "service": service,
                    "memo": rec_data["memo"]
                }
            except Exception as e:
                rep.message = {'msg': [{'message': str(e)}]}
        else:
            error_dict = form.errors.as_json()
            rep.message = json.loads(error_dict)
        return HttpResponse(json.dumps(rep.__dict__))

