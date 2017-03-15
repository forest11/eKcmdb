#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin

from database import models
from pagination.pager import PageInfo
from backend.response import BaseResponse
from django.http.request import QueryDict
from web.configure.base import BaseList


class User(BaseList):
    def __init__(self):
        # 查询条件的配置
        condition_config = [
            # name对应的值必须为数据库中可查询的字段，text的值为标签默认显示的文字，对应值为空
            # condition_type为select时，必须要指定global_name，且对应的值会返回给前端，如：'global_name': 'role_list'，
            # User类中有静态属性role_list
            {'name': 'name', 'text': '用户名', 'condition_type': 'input'},
            {'name': 'role__id', 'text': '角色', 'condition_type': 'select', 'global_name': 'role_list'},
            {'name': 'is_active', 'text': '状态', 'condition_type': 'select', 'global_name': 'status_list'},
        ]

        # 表格的配置
        table_config = [
            {
                'q': 'id',  # 用于数据库查询的字段，即Model.Tb.objects.filter(*[])，为None时，该字段不会查询
                'title': "ID",  # 前段表格中显示的标题
                'display': 1,  # 是否在前段显示，0表示在前端不显示, 非0表示前端显示
                'text': {'content': "{id}", 'kwargs': {'id': '@id'}},  #前端表格第1行显示字段，content为显示的具体文字，
                                                    # kwargs为content的变量替换，即{id}最后会被@id的对应替换，显示在前端
                'attr': {}  # 自定义属性
            },
            {
                'q': 'name',
                'title': "用户名",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@name'}},
                'attr': {}
            },
            {
                'q': 'department',
                'title': "部门",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@department_list'}},
                'attr': {}
            },
            {
                'q': 'email',
                'title': "Email",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@email'}},
                'attr': {}
            },
            {
                'q': 'mobile',
                'title': "手机号码",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@mobile'}},
                'attr': {}
            },
            {
                'q': 'role',
                'title': "角色",
                'display': 1,
                'separated': '、',
                'text': {'content': "{n}", 'kwargs': {'n': '@@@role_list'}},
                'attr': {'style': 'color: #2a67bb;'}
            },
            {
                'q': 'is_active',
                'title': "状态",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@status_list'}},
                'attr': {}
            },
            {
                'q': None,
                'title': "选项",
                'display': 1,
                'text': {
                    'content': "<a class='btn btn-xs btn-info' href='/accounts/user_management/{n}/' target='_blank'><i class='fa fa-paste'></i>编辑</a> <button type='button' class='btn btn-xs btn-danger demo3'><i class='fa fa-warning'></i>删除</a>",
                    'kwargs': {'n': '@id'}},
                'attr': {'class': 'col-sm-2'}
            },
        ]
        super(User, self).__init__(condition_config, table_config)

    @property
    def status_list(self):
        result = [{'id': 1, 'name': '正常'}, {'id': 0, 'name': '禁用'}]
        return result

    @property
    def role_list(self):
        values = models.Role.objects.values('id', 'name')
        return list(values)

    @property
    def department_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.UserProfile.department_choices)
        return list(result)

    def fetch_users(self, request):
        response = BaseResponse()
        try:
            ret = {}
            conditions = self.select_condition(request)
            user_count = models.UserProfile.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), user_count)
            sql_list = models.UserProfile.objects.filter(conditions).values(*self.values_list)
            user_list = self.handle_m2m_filed(list(sql_list))[page_info.start:page_info.end]
            ret['data_list'] = user_list
            ret['table_config'] = self.table_config
            ret['condition_config'] = self.condition_config
            ret['page_info'] = {
                "page_str": page_info.pager(),
                "page_start": page_info.start,
            }
            ret['global_dict'] = {
                'status_list': self.status_list,
                'role_list': self.role_list,
                'department_list': self.department_list,
            }
            response.data = ret
            response.message = '获取成功'
            response.status = True

        except Exception as e:
            response.message = str(e)
        return response

    @staticmethod
    def delete_user(request):
        response = BaseResponse()
        try:
            delete_dict = QueryDict(request.body, encoding='utf-8')
            id_list = delete_dict.getlist('id_list')
            models.UserProfile.objects.filter(id__in=id_list).delete()
            response.message = '删除成功'
            response.status = True
        except Exception as e:
            response.message = str(e)
        return response


class Role(BaseList):
    def __init__(self):
        condition_config = [
            {'name': 'name', 'text': '角色名', 'condition_type': 'input'},
        ]

        table_config = [
            {
                'q': 'id',
                'title': "ID",
                'display': 1,
                'text': {'content': "{id}", 'kwargs': {'id': '@id'}},
                'attr': {'class': 'col-sm-1'}
            },
            {
                'q': 'name',
                'title': "角色名",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@name'}},
                'attr': {'class': 'col-sm-2'}
            },
            {
                'q': 'perm',
                'title': "权限",
                'display': 1,
                'separated': ' | ',
                'text': {'content': "{n}", 'kwargs': {'n': '@@@perm_list'}},
                'attr': {'style': 'color: #2a67bb;'}
            },
            {
                'q': None,
                'title': "选项",
                'display': 1,
                'text': {
                    'content': "<a class='btn btn-xs btn-info' href='/accounts/role_management/{n}/' target='_blank'><i class='fa fa-paste'></i>编辑</a> <button type='button' class='btn btn-xs btn-danger demo3'><i class='fa fa-warning'></i>删除</a>",
                    'kwargs': {'n': '@id'}},
                'attr': {'class': 'col-sm-2'}
            },
        ]
        super(Role, self).__init__(condition_config, table_config)

    @property
    def perm_list(self):
        values = models.Permission.objects.only('id', 'caption')
        result = map(lambda x: {'id': x.id, 'name': x.caption}, values)
        return list(result)

    def fetch_roles(self, request):
        response = BaseResponse()
        try:
            ret = {}
            conditions = self.select_condition(request)
            role_count = models.Role.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), role_count)
            sql_list = models.Role.objects.filter(conditions).values(*self.values_list)
            role_list = self.handle_m2m_filed(list(sql_list))[page_info.start:page_info.end]
            ret['data_list'] = role_list
            ret['table_config'] = self.table_config
            ret['condition_config'] = self.condition_config
            ret['page_info'] = {
                "page_str": page_info.pager(),
                "page_start": page_info.start,
            }
            ret['global_dict'] = {
                'perm_list': self.perm_list
            }
            response.data = ret
            response.message = '获取成功'
            response.status = True
        except Exception as e:
            response.message = str(e)
        return response

    @staticmethod
    def delete_role(request):
        response = BaseResponse()
        try:
            delete_dict = QueryDict(request.body, encoding='utf-8')
            id_list = delete_dict.getlist('id_list')
            models.Role.objects.filter(id__in=id_list).delete()
            response.message = '删除成功'
            response.status = True
        except Exception as e:
            response.message = str(e)
        return response


class Permission(BaseList):
    def __init__(self):
        condition_config = [
            {'name': 'caption', 'text': '权限', 'condition_type': 'input'},
            {'name': 'code', 'text': 'url权限', 'condition_type': 'input'},
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
                'q': 'caption',
                'title': "权限描述",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@caption'}},
                'attr': {}
            },
            {
                'q': 'code',
                'title': "url权限",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@code'}},
                'attr': {}
            },
            {
                'q': 'method',
                'title': "请求方法",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@method'}},
                'attr': {}
            },
            {
                'q': 'kwargs',
                'title': "其他参数",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@kwargs'}},
                'attr': {}
            },
            {
                'q': None,
                'title': "选项",
                'display': 1,
                'text': {
                    'content': "<button class='btn btn-xs btn-info' type='button' data-toggle='modal' onclick='updatePermButton(this);'><i class='fa fa-paste'></i>编辑</button> <button type='button' class='btn btn-xs btn-danger demo3'><i class='fa fa-warning'></i>删除</a>",
                    'kwargs': {'n': '@id'}},
                'attr': {'class': 'col-sm-2'}
            },
        ]
        super(Permission, self).__init__(condition_config, table_config)

    def fetch_perms(self, request):
        response = BaseResponse()
        try:
            ret = {}
            conditions = self.select_condition(request)
            perm_count = models.Permission.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), perm_count)
            sql_list = models.Permission.objects.filter(conditions).values(*self.values_list)
            perm_list = self.handle_m2m_filed(list(sql_list))[page_info.start:page_info.end]
            ret['data_list'] = perm_list
            ret['table_config'] = self.table_config
            ret['condition_config'] = self.condition_config
            ret['page_info'] = {
                "page_str": page_info.pager(),
                "page_start": page_info.start,
            }
            ret['global_dict'] = {}
            response.data = ret
            response.message = '获取成功'
            response.status = True
        except Exception as e:
            response.message = str(e)
        return response

    @staticmethod
    def delete_perm(request):
        response = BaseResponse()
        try:
            delete_dict = QueryDict(request.body, encoding='utf-8')
            id_list = delete_dict.getlist('id_list')
            models.Permission.objects.filter(id__in=id_list).delete()
            response.message = '删除成功'
            response.status = True
        except Exception as e:
            response.message = str(e)
        return response