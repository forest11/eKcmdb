import json
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Q
from assets import models, forms
from backend.response import BaseResponse


@login_required
def index(request):
    return redirect("dashboard")


@login_required
def dashboard(request):
    """
    仪表盘
    :param request:
    :return:
    """
    hosts = models.Host.objects.all().count()
    users = models.UserProfile.objects.all().count()
    return render(request, 'common/dashboard.html', locals())


@login_required
def host_list(request):
    """
    主机列表页
    :param request:
    :return:
    """
    idcs = models.IDC.objects.all()
    business_units = models.BusinessUnit.objects.all()
    services = models.Service.objects.all()
    status = models.Host.status_choices
    return render(request, 'assets/host_list.html', locals())


def select_q(request, q, field_list):
    """
    构造过滤条件
    :param request:
    :param q:
    :param field_list:
    :return:
    """
    for item in [(x, request.GET.get(x)) for x in field_list]:
        if item[1]:
            q.children.append((item[0], item[1]))
    return q


@login_required
def iframe_host_list(request):
    """
    主机列表页通过iframe获取数据
    :param request:
    :return:
    """
    status = models.Host.status_choices
    if request.GET.get("ip_or_hostname"):
        q = Q()
        q.connector = "OR"
        q.children.append(('ip__contains', request.GET["ip_or_hostname"]))
        q.children.append(('hostname__contains', request.GET["ip_or_hostname"]))
    else:
        q1 = Q()
        q1.connector = "AND"
        q = select_q(request, q1, ["idc", "service__id", "status"])
    hosts = models.Host.objects.filter(q)
    hosts_physical = hosts.filter(is_virtual=False).count()
    hosts_virtual = hosts.filter(is_virtual=True).count()
    hosts_count = hosts.count()
    paginator = Paginator(hosts, 10)
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
    """
    添加主机
    :param request:
    :return:
    """
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
                        ip=rec_data['ip'],
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
def host_detail(request, host_id):
    """
    主机详细信息
    :param request:
    :param host_id:
    :return:
    """
    status = models.Host.status_choices
    host_obj = get_object_or_404(models.Host, id=host_id)
    return render(request, 'assets/host_detail.html', locals())


@login_required
def host_edit(request, host_id):
    """
    修改主机
    :param request:
    :param host_id:
    :return:
    """
    host_obj = get_object_or_404(models.Host, id=host_id)
    if request.method == 'GET':
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
        form = forms.HostEdit(request.POST, instance=host_obj)
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


@login_required
def host_del(request):
    """
    删除主机
    :param request:
    :return:
    """
    if request.method == 'POST':
        host_id = request.POST.get('id')
        del_host = models.Host.objects.filter(id=host_id).delete()
        if del_host:
            return HttpResponse(204)
    return HttpResponse(500)


@login_required
def host_update(request):
    """
    主动更新主机基础信息，暂时使用
    :param request:
    :return:
    """
    if request.method == 'POST':
        host_id = request.POST.get('id')
    return HttpResponse('host_update')


@login_required
def network_list(request):
    network_devices = models.NetDevice.objects.all()
    status = models.NetDevice.status_choices
    return render(request, 'common/index.html', locals())


@login_required
def network_add(request):
    status = models.NetDevice.status_choices
    idcs = models.IDC.objects.all()
    manufactorys = models.Manufactory.objects.all()
    return render(request, 'common/index.html', locals())


@login_required
def network_detail(request, network_id):
    status = models.NetDevice.status_choices
    if network_id:
        network_obj = models.NetDevice.objects.get(id=network_id)
    return render(request, 'assets/network_detail.html', locals())


@login_required
def network_update(request):
    return render(request, 'assets/network_list.html')


@login_required
def network_del(request):
    return render(request, 'assets/network_list.html')

