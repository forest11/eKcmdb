#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin

from django.shortcuts import render
from backend.utils import ResolveUrl


def check_auth(func):

    """
    权限认证
    :param func:
    :return:
    """

    def wrapper(request, *args, **kwargs):
        cur_url = request.path_info
        perm_list = request.session.get('perm_list')
        if perm_list:

            if cur_url not in ResolveUrl.url(perm_list):
                return render(request, 'default/403.html', status=403)
        else:
            return render(request, 'default/403.html', status=403)
        return func(request, *args, **kwargs)
    return wrapper