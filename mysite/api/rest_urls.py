#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
from django.conf.urls import url, include
from rest_framework import routers
from api import rest_views

router = routers.DefaultRouter()
router.register(r'assets_view', rest_views.HostView)
router.register(r'users_view', rest_views.UserView)
router.register(r'role_view', rest_views.RoleView)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^assets_list/$', rest_views.HostList, name="assets_list"),
    url(r'^users_list/$', rest_views.UserList, name="users_list"),
    url(r'^assets-auth/', include('rest_framework.urls', namespace='rest_framework'))   #api安全认证
]