#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin

import json
from database import models
from pagination.pager import PageInfo
from backend.response import BaseResponse
from django.http.request import QueryDict
from web.configure.base import BaseList


class Host(BaseList):
    def __init__(self):
        # 查询条件的配置
        condition_config = [
            {'name': 'ip', 'text': 'ip', 'condition_type': 'input'},
            {'name': 'idc', 'text': '机房', 'condition_type': 'select', 'global_name': 'idc_list'},
            {'name': 'status', 'text': '资产状态', 'condition_type': 'select', 'global_name': 'status_list'},
        ]
        
        # 表格的配置
        table_config = [
            {
                'q': 'id',
                'title': "ID",
                'display': 1,
                'text': {'content': "{id}", 'kwargs': {'id': '@id'}},
                'attr': {}
            },
            {
                'q': 'hostname',
                'title': "主机名",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@hostname'}},
                'attr': {}
            },
            {
                'q': 'ip',
                'title': "ip",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@ip'}},
                'attr': {}
            },
            {
                'q': 'sn',
                'title': "sn",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@sn'}},
                'attr': {}
            },
            {
                'q': 'idc_id',
                'title': "IDC",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@idc_list'}},
                'attr': {}
            },
            {
                'q': 'status',
                'title': "资产状态",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@status_list'}},
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
                    'content': "<a class='btn btn-xs btn-primary' href='/assets/host_detail.html?id={n}' target='_blank'>查看详细</a> <a class='btn btn-xs btn-info' href='/assets/host_update.html?id={n}' target='_blank'><i class='fa fa-paste'></i>编辑</a> <button type='button' class='btn btn-xs btn-danger demo3'><i class='fa fa-warning'></i>删除</a>",
                    'kwargs': {'n': '@id'}},
                'attr': {'class': 'col-sm-2'}
            },
        ]
        super(Host, self).__init__(condition_config, table_config)

    @property
    def status_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.Host.status_choices)
        return list(result)

    @property
    def idc_list(self):
        values = models.IDC.objects.only('id', 'name', 'address')
        result = map(lambda x: {'id': x.id, 'name': "%s-%s" % (x.name, x.address)}, values)
        return list(result)

    def fetch_assets(self, request):
        response = BaseResponse()
        try:
            ret = {}
            conditions = self.select_condition(request)
            asset_count = models.Host.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), asset_count)
            sql_list = models.Host.objects.filter(conditions).values(*self.values_list)
            host_list = self.handle_m2m_filed(list(sql_list))[page_info.start:page_info.end]
            ret['data_list'] = host_list
            ret['table_config'] = self.table_config
            ret['condition_config'] = self.condition_config
            ret['page_info'] = {
                "page_str": page_info.pager(),
                "page_start": page_info.start,
            }
            ret['global_dict'] = {
                'status_list': self.status_list,
                'idc_list': self.idc_list,
            }
            response.data = ret
            response.message = '获取成功'
            response.status = True

        except Exception as e:
            response.message = str(e)
        return response

    @staticmethod
    def delete_assets(request):
        response = BaseResponse()
        try:
            delete_dict = QueryDict(request.body, encoding='utf-8')
            id_list = delete_dict.getlist('id_list')
            models.Host.objects.filter(id__in=id_list).delete()
            response.message = '删除成功'
            response.status = True
        except Exception as e:
            response.message = str(e)
        return response

    @staticmethod
    def put_assets(request):
        response = BaseResponse()
        try:
            response.error = []
            put_data = QueryDict(request.body, encoding='utf-8')
            update_list = json.loads(put_data.get('data'))
            for row_dict in update_list:
                id = row_dict.pop('id')
                try:
                    models.Host.objects.filter(id=id).update(**row_dict)
                except Exception as e:
                    response.message = str(e)
            response.message = '更新成功'
            response.status = True
        except Exception as e:
            response.message = str(e)
        return response

    @staticmethod
    def assets_detail(asset_id):
        response = BaseResponse()
        try:
            response.data = models.Host.objects.filter(asset_id=asset_id).select_related('asset').first()
            response.status = True
        except Exception as e:
            response.message = str(e)
        return response
