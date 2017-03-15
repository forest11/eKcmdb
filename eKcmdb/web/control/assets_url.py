# -*- coding: utf-8 -*-
# __Author__: PanDongLin
from django.conf.urls import url
from web.views import assets


urlpatterns = [
    url(r'^index.html', assets.index, name='index'),
    url(r'^host_list.html', assets.HostList.as_view(), name='host_list'),
    url(r'^host_json_list.html', assets.HostJsonList.as_view(), name='host_json_list'),
    url(r'^host_detail/(?P<host_id>\d+).html', assets.HostDetail.as_view(), name='host_detail'),
    url(r'^host_add.html$', assets.HostAdd.as_view(), name='host_add'),
    url(r'^host_management/(?P<host_id>\d+)/', assets.HostManagement.as_view(), name='host_management'),
    url(r'^host_update/', assets.HostUpdate.as_view(), name='host_update'),
    url(r'^network_list/', assets.network_list, name='network_list'),
    url(r'^network_detail/(?P<network_id>\d+)/', assets.network_detail, name='network_detail'),
    url(r'^network_add/', assets.network_add, name='network_add'),
    url(r'^network_management/', assets.network_update, name='network_management'),
]
