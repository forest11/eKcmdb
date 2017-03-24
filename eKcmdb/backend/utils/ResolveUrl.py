#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
from django.urls import reverse as url_reverse


def url(url_list):
    temp_list = []
    for i in url_list:
        try:
            url = url_reverse(i)
            temp_list.append(url)
        except:
            pass
    return temp_list