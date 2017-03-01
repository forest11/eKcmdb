# -*- coding: utf-8 -*-
# __Author__: PanDongLin
from django.conf.urls import url
from common import views

urlpatterns = [
    url(r'^business_list/', views.business_list, name='business_list'),
    url(r'^business_add/', views.business_add, name='business_add'),
    url(r'^business_del/', views.business_del, name='business_del'),
    url(r'^business_update/(?P<business_id>\d+)/', views.business_update),
    url(r'^service_list/', views.service_list, name='service_list'),
    url(r'^service_add/', views.service_add, name='service_add'),
    url(r'^service_del/', views.service_del, name='service_del'),
    url(r'^service_update/(?P<service_id>\d+)/', views.service_update),
]
