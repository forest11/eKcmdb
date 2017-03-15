#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin

from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger


def split_page(obj, current_page_num, page_num=10):
    paginator = Paginator(obj, page_num)
    try:
        page_obj = paginator.page(current_page_num)
    except (InvalidPage, PageNotAnInteger):
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj