#!/usr/bin/env python3
# -*— coding: utf-8 -*-
# __author__ : pandonglin
from django import template

register = template.Library()


@register.filter
def make_null(args):
    return ''
