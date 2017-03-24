# -*- coding: utf-8 -*-
# __Author__: PanDongLin
from django.conf.urls import url
from web.views import assets


urlpatterns = [
    url(r'^index.html$', assets.index, name='index'),
    url(r'^host_list.html$', assets.HostList.as_view(), name='host_list'),
    url(r'^host_json_list.html$', assets.HostJsonList.as_view(), name='host_json_list'),
    url(r'^host_detail.html$', assets.HostDetail.as_view(), name='host_detail'),
    url(r'^host_add.html$', assets.HostAdd.as_view(), name='host_add'),
    url(r'^host_update.html$', assets.HostUpdate.as_view(), name='host_update'),
    url(r'^host_grain.html$', assets.HostGrain.as_view(), name='host_grain'),
]
