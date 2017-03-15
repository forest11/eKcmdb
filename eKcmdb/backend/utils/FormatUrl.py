#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin


def format_url(url_dict):
    """
    格式化url
    :param url_dict:
    :return:
    """
    key = "%s" % url_dict['perm__code']
    value = {"method": url_dict['perm__method'], 'kwargs': url_dict['perm__kwargs']}
    return key, value


def ret_url_method(perm_list):
    """
    权限列表格式化为字典类型
    :param perm_list:
    :return:
    """
    perm_dict = {}
    for item in perm_list:
        key, value = format_url(item)
        perm_dict[key] = value
    return perm_dict