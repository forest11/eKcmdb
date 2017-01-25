# -*- coding: utf-8 -*-
# __Author__: PanDongLin
from django.conf.urls import url
from autoops import views


urlpatterns = [
    url(r'^multi_cmd/', views.multi_cmd, name='multi_cmd'),
    url(r'^task_center/$', views.task_center, name="task_center"),
    url(r'^task_center/result/$', views.get_task_result, name="get_task_result"),
]