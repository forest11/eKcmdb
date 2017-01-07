from django.shortcuts import render


def product_detail(request):
    return render(request, 'monitor/product_detail.html')
