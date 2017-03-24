#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin

from django.conf.urls import url
from web.views import monitors

urlpatterns = [
    url(r'^monitor-detail.html$', monitors.MonitorDetail.as_view(), name='monitor-detail'),
    url(r'^zabbix.html$', monitors.ZabbixList.as_view(), name='zabbix'),
]