# -*- coding: utf-8 -*-
# __Author__: PanDongLin
from django.conf.urls import url
from monitor import views


urlpatterns = [
    url(r'^product-detail/', views.product_detail, name='product-detail'),
]