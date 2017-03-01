from django.shortcuts import render


def product_detail(request):
    return render(request, 'monitor/product_detail.html')


def zabbix(request):
    return render(request, 'common/index.html')