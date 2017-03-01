# -*- coding: utf-8 -*-
# __Author__: PanDongLin
from django.conf.urls import url, include
from assets import views


urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^dashboard/', views.dashboard, name='dashboard'),
    url(r'^host_list/', views.host_list, name='host_list'),
    url(r'^iframe_host_list/', views.iframe_host_list, name='iframe_host_list'),
    url(r'^host_detail/(?P<host_id>\d+)/', views.host_detail),
    url(r'^host_add/', views.host_add, name='host_add'),
    url(r'^host_edit/(?P<host_id>\d+)/', views.host_edit),
    url(r'^host_del/', views.host_del, name='host_del'),
    url(r'^host_update/', views.host_update, name='host_update'),
    url(r'^network_list/', views.network_list, name='network_list'),
    url(r'^network_detail/(?P<network_id>\d+)/', views.network_detail),
    url(r'^network_add/', views.network_add, name='network_add'),
    url(r'^network_update/', views.network_update, name='network_update'),
    url(r'^network_del/', views.network_del, name='network_del'),
]