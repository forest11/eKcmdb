#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
import re
from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def guess_page(current_page, loop_num):
    """分页"""
    offset = abs(current_page-loop_num)
    if offset < 3:
        if current_page == loop_num:
            page_ele = '''<li class="paginate_button active"><a href="?page=%s">%s</a></li>''' % (loop_num, loop_num)
        else:
            page_ele = '''<li class="paginate_button"><a href="?page=%s">%s</a></li>''' % (loop_num, loop_num)
        return format_html(page_ele)
    else:
        return ''