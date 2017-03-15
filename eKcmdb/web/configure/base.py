#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.db.models import Q


class BaseList(object):
    def __init__(self, condition_config, table_config):
        # 查询条件的配置，列表
        self.condition_config = condition_config

        # 表格的配置，列表
        """
        {
            'q': 'title',       # 用于数据库查询的字段，即Model.Tb.objects.xxx.values(*['v',]), None则表示不获取相应的数据库列
            'title': '标题',     # table表格显示的列名
            'display': 0        # 实现在表格中显示 0，不显示；1显示
            'text': {'content': "{id}", 'kwargs': {'id': '@id'}}, # 表格的每一个td中显示的内容,一个@表示获取数据库查询字段，两个@@，表示根据当前id在全局变量中找到id对应的内容
            'attr': {}          # 自定义属性
        }
        """
        self.table_config = table_config

    @property
    def values_list(self):
        """
        数据库查询时的指定字段
        :return:
        """
        values = []
        for item in self.table_config:
            if item['q']:
                values.append(item['q'])
        return values

    @staticmethod
    def select_condition(request):
        """
        查询条件处理
        :param request:
        :return:
        """
        con_str = request.GET.get('condition', None)
        if not con_str:
            con_dict = {}
        else:
            con_dict = json.loads(con_str)

        con_q = Q()
        for k, v in con_dict.items():
            temp = Q()
            temp.connector = 'OR'
            for item in v:
                temp.children.append((k, item))
            con_q.add(temp, 'AND')

        return con_q

    @staticmethod
    def handle_m2m_filed(dict_list):
        """
        对查询结果中可能含有的多对多字段进行处理
        :param dict_list:
        :return:
        """
        id_list = []
        m2m_filed_dict = []
        new_dict_list = []

        for dic in dict_list:
            id = dic['id']
            if id in id_list:
                m2m_filed_dict = new_dict_list[id_list.index(id)]
                for k, v in dic.items():
                    if k in m2m_filed_dict and v not in m2m_filed_dict[k]:
                        m2m_filed_dict[k].append(v)

            else:
                id_list.append(id)
                new_dict = {}
                for k, v in dic.items():
                    new_dict[k] = [v]
                new_dict_list.append(new_dict)

        for dic in new_dict_list:
            for x, y in dic.items():
                if len(dic[x]) == 0:
                    dic[x] = None
                elif len(dic[x]) == 1:
                    dic[x] = y[0]
        return new_dict_list

