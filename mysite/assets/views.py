import json
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from assets import models, forms
from backend.response import BaseResponse



@login_required
def index(request):
    return render(request, 'common/index.html')


@login_required
def dashboard(request):
    hosts = models.Host.objects.all().count()
    users = models.UserProfile.objects.all().count()
    return render(request, 'common/dashboard.html', locals())


@login_required
def host_list(request):
    idcs = models.IDC.objects.all()
    business_units = models.BusinessUnit.objects.all()
    services = models.Service.objects.all()
    status = models.Host.status_choices
    return render(request, 'assets/host_list.html', locals())


def select_q(request, field_list):
    q = {}
    for item in [(x, request.GET.get(x)) for x in field_list]:
        if item[1]:
            q[item[0]] = item[1]
    return q


@login_required
def iframe_host_list(request):
    hosts_physical = models.Host.objects.filter(is_virtual=False).count()
    hosts_virtual = models.Host.objects.filter(is_virtual=True).count()
    status = models.Host.status_choices
    q = select_q(request, ["idc", "service__id", "status"])
    hosts = models.Host.objects.filter(**q)
    hosts_count = hosts.count()
    paginator = Paginator(hosts, 5)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except (InvalidPage, PageNotAnInteger):
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'assets/iframe_host_list.html', locals())


@login_required
def host_add(request):
    if request.method == 'GET':
        device_types = models.Host.device_type_choices
        status = models.Host.status_choices
        idcs = models.IDC.objects.all()
        manufactories = models.Manufactory.objects.all()
        return render(request, 'assets/host_add.html', locals())
    elif request.method == 'POST':
        rep = BaseResponse()
        form = forms.HostAdd(request.POST)
        if form.is_valid():
            rec_data = form.clean()
            try:
                host_obj = models.Host(
                        sn=rec_data['sn'],
                        number=rec_data['number'],
                        qs=rec_data['qs'],
                        hostname=rec_data['hostname'],
                        asset_name=rec_data['asset_name'],
                        management_ip=rec_data['management_ip'],
                        is_virtual=rec_data['is_virtual'],
                        cabinet=rec_data['cabinet'],
                        host_cabinet_id=rec_data['host_cabinet_id'],
                        status=rec_data['status'],
                        buy_date=rec_data['buy_date'],
                        memo=rec_data['memo'],
                )
                host_obj.idc = models.IDC.objects.get(id=rec_data['idc'])
                host_obj.manufactory = models.Manufactory.objects.get(id=rec_data['manufactory'])
                host_obj.save()
                rep.status = True
            except Exception as e:
                rep.message = {'msg': [{'message': str(e)}]}
        else:
            error_dict = form.errors.as_json()
            rep.message = json.loads(error_dict)
        return HttpResponse(json.dumps(rep.__dict__))


@login_required
def host_detail(request):
    host_id = request.GET.get('id', None)
    status = models.Host.status_choices
    if host_id:
        host_obj = get_object_or_404(models.Host, id=host_id)
    return render(request, 'assets/host_detail.html', locals())


@login_required
def host_edit(request):
    if request.method == 'GET':
        host_obj = get_object_or_404(models.Host, id=request.GET.get('id'))
        idcs = models.IDC.objects.all()
        business_units = models.BusinessUnit.objects.all()
        services = models.Service.objects.all()
        device_types = models.Host.device_type_choices
        raid_types = models.Host.raid_type_choices
        status = models.Host.status_choices
        os_types = models.System.objects.all()
        manufactories = models.Manufactory.objects.all()
        return render(request, 'assets/host_edit.html', locals())
    elif request.method == 'POST':
        rep = BaseResponse()
        host_obj = get_object_or_404(models.Host, id=request.POST.get('id', None))

        form = forms.HostEdit(request.POST, instance=host_obj)
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
def host_del(request):
    if request.method == 'POST':
        host_id = request.POST.get('id')
        del_host = models.Host.objects.filter(id=host_id).delete()
        if del_host:
            return HttpResponse(204)
    return HttpResponse(500)


@login_required
def host_update(request):
    if request.method == 'POST':
        host_id = request.POST.get('id')
    return HttpResponse('host_update')


@login_required
def network_list(request):
    network_devices = models.Device.objects.all()
    status = models.Device.status_choices
    return render(request, 'common/index.html', locals())


@login_required
def network_add(request):
    status = models.Device.status_choices
    idcs = models.IDC.objects.all()
    manufactorys = models.Manufactory.objects.all()
    return render(request, 'common/index.html', locals())


@login_required
def network_detail(request):
    network_id = request.GET.get('id', None)
    status = models.Device.status_choices
    if network_id:
        network_obj = models.Device.objects.get(id=network_id)
    return render(request, 'assets/network_detail.html', locals())


@login_required
def network_edit(request):
    return render(request, 'assets/network_list.html')


@login_required
def network_del(request):
    return render(request, 'assets/network_list.html')

