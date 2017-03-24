#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin

from django.conf.urls import url
from web.views import devops


urlpatterns = [
    url(r'^business_list.html$', devops.BusinessList.as_view(), name='business_list'),
    url(r'^business_add.html$', devops.BusinessAdd.as_view(), name='business_add'),
    url(r'^business_update.html$', devops.BusinessUpdate.as_view(), name='business_update'),
    url(r'^service_list.html$', devops.ServiceList.as_view(), name='service_list'),
    url(r'^server_json_list.html$', devops.ServiceJsonList.as_view(), name='server_json_list'),
    url(r'^service_add.html$', devops.ServiceAdd.as_view(), name='service_add'),
    url(r'^service_update.html$', devops.ServiceUpdate.as_view(), name='service_update'),
    url(r'^check_sql.html', devops.CheckSql.as_view(), name='check_sql'),
    url(r'^sql_log.html', devops.SqlLog.as_view(), name='sql_log'),
    url(r'^show_message.html', devops.ShowMessage.as_view(), name='show_message'),
    url(r'^code_ops.html', devops.CodeOps.as_view(), name='code_ops'),
    url(r'^code_log.html', devops.CodeLog.as_view(), name='code_log'),
    url(r'^multi_cmd.html', devops.MuliCmd.as_view(), name='multi_cmd'),
    url(r'^task_center.html$', devops.task_center, name="task_center"),
    url(r'^task_center/result/$', devops.get_task_result, name="get_task_result"),
]