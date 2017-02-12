#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin


def session_perm_list(request):
    """
    所有的templates中都可以使用，等效全局变量，返回值必须使字典类型的值,如{"data": data}

    """
    return locals()