# -*- coding: utf-8 -*-
# __Author__: PanDongLin
from django.conf.urls import url
from accounts import views

urlpatterns = [
    url(r'^login/', views.user_login, name='login'),
    url(r'^logout/', views.user_logout,  name='logout'),
    url(r'^change_pwd/', views.change_pwd, name='change_pwd'),
    url(r'^send_msg/', views.send_msg, name='send_msg'),
    url(r'^forget_pwd/', views.forget_pwd, name='forget_pwd'),
    url(r'^reset_pwd/', views.reset_pwd, name='reset_pwd'),
    url(r'^show_message/', views.show_message, name='show_message'),
    url(r'^user_list/', views.user_list, name='user_list'),
    url(r'^user_add/', views.user_add, name='user_add'),
    url(r'^user_del/', views.user_del, name='user_del'),
    url(r'^user_update/', views.user_update, name='user_update'),
    url(r'^role_list/', views.role_list, name='role_list'),
    url(r'^permission_list/', views.permission_list, name='permission_list'),
]
