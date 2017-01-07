#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
from django.conf.urls import url, include
from rest_framework import routers
from api.assets import rest_views

router = routers.DefaultRouter()
router.register(r'assets', rest_views.HostViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'assets_list/$', rest_views.HostList),
    url(r'^assets-auth/', include('rest_framework.urls', namespace='rest_framework'))   #api安全认证
]