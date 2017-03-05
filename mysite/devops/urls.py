# -*- coding: utf-8 -*-
# __Author__: PanDongLin
from django.conf.urls import url
from devops import views


urlpatterns = [
    url(r'^show_message/', views.show_message, name='show_message'),
    url(r'^multi_cmd/', views.multi_cmd, name='multi_cmd'),
    url(r'^task_center/$', views.task_center, name="task_center"),
    url(r'^task_center/result/$', views.get_task_result, name="get_task_result"),
    url(r'^code_commit/', views.code_commit, name='code_commit'),
    url(r'^code_audit/', views.code_audit, name='code_audit'),
    url(r'^code_list/', views.code_list, name='code_list'),
]