#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
import re
from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def guess_page(request, paginator_obj, loop_counter):
    """分页"""
    abs_full_url = request.get_full_path()

    if "?page=" in abs_full_url:
        url = re.sub("page=\d+", "page=%s" % loop_counter, request.get_full_path())
    elif "?" in abs_full_url:
        url = "%s&page=%s" % (request.get_full_path(), loop_counter)
    else:
        url = "%s?page=%s" % (request.get_full_path(), loop_counter)

    if loop_counter == paginator_obj.number: #current page
        page_ele = '''<li class='active'><a href="{abs_url}">{page_num}</a></li>'''.format(abs_url=url,
                                                                                            page_num=loop_counter)
        return format_html(page_ele)

    offset = abs(paginator_obj.number - loop_counter)

    if offset < 2 or loop_counter == 1 or loop_counter == paginator_obj.paginator.num_pages:
        page_ele = '''<li><a href="{abs_url}">{page_num}</a></li>'''.format(abs_url=url, page_num=loop_counter)

    elif offset < 3:
        page_ele = '''<li><a href="{abs_url}">...</a></li>'''.format(abs_url=url, page_num=loop_counter)

    else:
        page_ele = ''
    return format_html(page_ele)


@register.simple_tag
def filter_page(request, page_num):
    """替换url中的page的值"""
    abs_full_url = request.get_full_path()

    if "?page=" in abs_full_url:
        url = re.sub("page=\d+", "page=%s" % page_num, request.get_full_path())
    elif "?" in abs_full_url:
        url = "%s&page=%s" % (request.get_full_path(), page_num)
    else:
        url = "%s?page=%s" % (request.get_full_path(), page_num)
    return format_html(url)