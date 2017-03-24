# -*- coding: utf-8 -*-
# __Author__: PanDongLin
from django.conf.urls import url
from web.views import accounts


urlpatterns = [
    url(r'^login.html$', accounts.LoginView.as_view(), name='login'),
    url(r'^logout.html$', accounts.LogoutView.as_view(),  name='logout'),
    url(r'^change_pwd.html$', accounts.ChangePassWd.as_view(), name='change_pwd'),
    url(r'^send_msg.html$', accounts.SendMsg.as_view(), name='send_msg'),
    url(r'^forget_pwd.html$', accounts.ForgetPassWd.as_view(), name='forget_pwd'),
    url(r'^reset_pwd.html$', accounts.RestPassWd.as_view(), name='reset_pwd'),
    url(r'^user_list.html$', accounts.UserList.as_view(), name='user_list'),
    url(r'^user_json_list.html$', accounts.UserJsonList.as_view(), name='user_json_list'),
    url(r'^user_add.html$', accounts.UserAdd.as_view(), name='user_add'),
    url(r'^user_update.html$', accounts.UserUpdate.as_view(), name='user_update'),
    url(r'^role_list.html$', accounts.RoleList.as_view(), name='role_list'),
    url(r'^role_json_list.html$', accounts.RoleJsonList.as_view(), name='role_json_list'),
    url(r'^role_add.html$', accounts.RoleAdd.as_view(), name='role_add'),
    url(r'^role_update.html$', accounts.RoleUpdate.as_view(), name='role_update'),
    url(r'^permission_list.html$', accounts.PermList.as_view(), name='permission_list'),
    url(r'^permission_json_list.html$', accounts.PermJsonList.as_view(), name='permission_json_list'),
    url(r'^permission_add.html$', accounts.PermAdd.as_view(), name='permission_add'),
    url(r'^permission_update.html$', accounts.PermUpdate.as_view(), name='permission_update'),
]
