#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin

from database import models
from pagination.pager import PageInfo
from backend.response import BaseResponse
from django.http.request import QueryDict
from web.configure.base import BaseList


class Service(BaseList):
    def __init__(self):
        condition_config = [
            {'name': 'name', 'text': '服务名', 'condition_type': 'input'},
            {'name': 'host__ip', 'text': '主机 ip', 'condition_type': 'input'},
        ]

        table_config = [
            {
                'q': 'id',
                'title': "ID",
                'display': 1,
                'text': {'content': "{id}", 'kwargs': {'id': '@id'}},
                'attr': {}
            },
            {
                'q': 'name',
                'title': "服务名",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@name'}},
                'attr': {}
            },
            {
                'q': 'host',
                'title': "主机",
                'display': 1,
                'separated': '、',
                'text': {'content': "{n}", 'kwargs': {'n': '@@@host_list'}},
                'attr': {'style': 'color: #2a67bb;'}
            },
            {
                'q': 'port',
                'title': "端口",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@port'}},
                'attr': {}
            },
            {
                'q': 'memo',
                'title': "备注",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@memo'}},
                'attr': {}
            },
            {
                'q': None,
                'title': "选项",
                'display': 1,
                'text': {
                    'content': "<a class='btn btn-xs btn-info' href='/devops/service_update.html?id={n}' target='_blank'><i class='fa fa-paste'></i>编辑</a> <button type='button' class='btn btn-xs btn-danger demo3'><i class='fa fa-warning'></i>删除</a>",
                    'kwargs': {'n': '@id'}},
                'attr': {'class': 'col-sm-2'}
            },
        ]
        super(Service, self).__init__(condition_config, table_config)

    @property
    def host_list(self):
        values = models.Host.objects.only('id', 'ip')
        result = map(lambda x: {'id': x.id, 'name': x.ip}, values)
        return list(result)

    def fetch_services(self, request):
        response = BaseResponse()
        try:
            ret = {}
            conditions = self.select_condition(request)
            perm_count = models.Service.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), perm_count)
            sql_list = models.Service.objects.filter(conditions).values(*self.values_list)
            ser_list = self.handle_m2m_filed(list(sql_list))[page_info.start:page_info.end]
            ret['data_list'] = ser_list
            ret['table_config'] = self.table_config
            ret['condition_config'] = self.condition_config
            ret['page_info'] = {
                "page_str": page_info.pager(),
                "page_start": page_info.start,
            }
            ret['global_dict'] = {
                'host_list': self.host_list
            }
            response.data = ret
            response.message = '获取成功'
            response.status = True
        except Exception as e:
            response.message = str(e)
        return response

    @staticmethod
    def delete_service(request):
        response = BaseResponse()
        try:
            delete_dict = QueryDict(request.body, encoding='utf-8')
            id_list = delete_dict.getlist('id_list')
            models.Service.objects.filter(id__in=id_list).delete()
            response.message = '删除成功'
            response.status = True
        except Exception as e:
            response.message = str(e)
        return response