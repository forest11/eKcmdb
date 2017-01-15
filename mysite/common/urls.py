# -*- coding: utf-8 -*-
# __Author__: PanDongLin
from django.conf.urls import url
from common import views

urlpatterns = [
    url(r'^business_list/', views.business_list, name='business_list'),
    url(r'^business_add/', views.business_add, name='business_add'),
    url(r'^service_list/', views.service_list, name='service_list'),
    url(r'^service_add/', views.service_add, name='service_add'),
]
