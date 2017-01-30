#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
from django.conf.urls import url, include
from rest_framework import routers
from api.assets import assets_views
from api.accounts import accounts_views

# router = routers.DefaultRouter()
# router.register(r'assets_list', assets_views.HostView)
# router.register(r'users_list', accounts_views.UserList)

urlpatterns = [
    # url(r'^', include(router.urls)),
    url(r'^assets_list/$', assets_views.HostList, name="assets_list"),
    url(r'^users_list/$', accounts_views.UserList, name="users_list"),
    url(r'^assets-auth/', include('rest_framework.urls', namespace='rest_framework'))   #api安全认证
]